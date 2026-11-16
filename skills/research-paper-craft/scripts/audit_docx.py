#!/usr/bin/env python3
"""Read-only DOCX structural preflight, not a Word renderer or a format fixer.

Findings are review candidates. Even zero findings do not approve typography,
pagination, scientific meaning, or anonymity. No manuscript excerpts are emitted.
Only transitional WordprocessingML DOCX is supported. No macros, links, or OLE
objects are executed. The complete style cascade is deliberately not simulated.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re
import sys
import xml.etree.ElementTree as ET
from zipfile import BadZipFile, ZipFile

W = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'
M = 'http://schemas.openxmlformats.org/officeDocument/2006/math'
WP = 'http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing'
NS = {'w': W, 'm': M, 'wp': WP}
MAX_ARCHIVE = 256 * 1024 * 1024
MAX_TOTAL = 256 * 1024 * 1024
MAX_XML = 8 * 1024 * 1024
MAX_XML_TOTAL = 32 * 1024 * 1024
MAX_ENTRIES = 4096


def tag(local: str) -> str:
    return '{' + W + '}' + local


def attr(element: ET.Element, name: str, default: str = '') -> str:
    return element.get(tag(name), default)


def enabled(element: ET.Element) -> bool:
    return attr(element, 'val', 'true').casefold() not in {'0', 'false', 'off'}


def digest_stream(stream) -> str:
    digest = hashlib.sha256()
    for chunk in iter(lambda: stream.read(1024 * 1024), b''):
        digest.update(chunk)
    return digest.hexdigest()


def parse_xml(data: bytes, name: str) -> ET.Element:
    # Remove NULs only for this security scan so UTF-16 declarations cannot hide a DTD.
    upper = data.replace(b'\x00', b'').upper()
    if b'<!DOCTYPE' in upper or b'<!ENTITY' in upper:
        raise ValueError(f'DTD/entity declarations are unsupported in {name}')
    try:
        return ET.fromstring(data)
    except ET.ParseError as error:
        raise ValueError(f'Malformed XML in {name}: {error}') from error


def audit_docx(path: Path | str) -> dict:
    """Inspect bounded ZIP/XML data without writing to the input or extracting files."""
    path = Path(path)
    if path.suffix.casefold() != '.docx':
        raise ValueError('Use an unencrypted .docx file, not DOC, DOCM, PDF, or an image.')
    if path.stat().st_size > MAX_ARCHIVE:
        raise ValueError('Archive exceeds the documented 256 MiB inspection limit.')
    with path.open('rb') as stream:
        initial_hash = digest_stream(stream)
    findings = []
    inventory = {'paragraphs': 0, 'tables': 0, 'equations': 0, 'drawings': 0,
                 'field_instructions': 0, 'bookmarks': 0, 'embedded_objects': 0,
                 'revisions': 0, 'external_relationships': 0}
    fonts = set()
    spacing_settings = []
    part_hashes = {}
    roots = {}

    def add(code: str, part: str, location: str, message: str, values=None):
        row = {'code': code, 'severity': 'review', 'part': part,
               'location': location, 'message': message}
        if values is not None:
            row['values'] = values
        findings.append(row)

    try:
        with ZipFile(path) as archive:
            infos = archive.infolist()
            names = [item.filename for item in infos]
            if len(names) != len(set(names)):
                raise ValueError('Duplicate ZIP entries make this package ambiguous.')
            if len(infos) > MAX_ENTRIES or sum(i.file_size for i in infos) > MAX_TOTAL:
                raise ValueError('Package exceeds entry or uncompressed-size limits.')
            if any(i.flag_bits & 1 for i in infos):
                raise ValueError('Encrypted ZIP entries are unsupported.')
            if not {'word/document.xml', '[Content_Types].xml'}.issubset(names):
                raise ValueError('Missing required DOCX package parts.')
            xml_total = 0
            for info in infos:
                if info.is_dir():
                    continue
                with archive.open(info) as stream:
                    part_hashes[info.filename] = digest_stream(stream)
                if not info.filename.endswith(('.xml', '.rels')):
                    continue
                xml_total += info.file_size
                if info.file_size > MAX_XML or xml_total > MAX_XML_TOTAL:
                    raise ValueError('XML exceeds the per-part or combined inspection limit.')
                roots[info.filename] = parse_xml(archive.read(info), info.filename)
    except (BadZipFile, RuntimeError) as error:
        raise ValueError(f'Cannot inspect DOCX package: {error}') from error

    if roots['word/document.xml'].tag != tag('document'):
        raise ValueError('Unsupported WordprocessingML namespace. Native Word review is required.')
    types = roots['[Content_Types].xml']
    if not any(e.get('PartName') == '/word/document.xml' and
               e.get('ContentType') == 'application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml'
               for e in types):
        raise ValueError('Main document content type is unsupported or not a standard DOCX.')

    for part, root in roots.items():
        for element in root.iter():
            if element.get('TargetMode') == 'External':
                inventory['external_relationships'] += 1
        if not part.startswith('word/') or not part.endswith('.xml'):
            continue
        parent = {child: element for element in root.iter() for child in element}
        paras = list(root.iter(tag('p')))
        para_id = {p: index for index, p in enumerate(paras, 1)}
        inventory['paragraphs'] += len(paras)
        counts = {'tbl':'tables', 'drawing':'drawings', 'instrText':'field_instructions',
                  'fldSimple':'field_instructions', 'bookmarkStart':'bookmarks',
                  'object':'embedded_objects', 'ins':'revisions', 'del':'revisions'}
        for local, key in counts.items():
            inventory[key] += sum(1 for _ in root.iter(tag(local)))
        inventory['equations'] += sum(1 for _ in root.iter('{' + M + '}oMath'))

        def location(element):
            here = element
            while here is not None:
                if here in para_id:
                    return f'paragraph[{para_id[here]}]'
                if here.tag == tag('style'):
                    return f'style[{attr(here, "styleId", "unnamed")}] definition'
                here = parent.get(here)
            return 'document or style settings'

        for p in paras:
            where = location(p)
            text = ''.join(e.text or '' for e in p.iter() if e.tag in {tag('t'), '{'+M+'}t'})
            if re.search(r' {2,}', text):
                add('REPEATED_SPACES', part, where, 'Inspect literal repeated spaces. Preserve intentional math, code, and alignment.')
            candidates = sorted(set(text) & {'¿', '□', '\ufffd'})
            if candidates:
                add('GLYPH_REVIEW', part, where, 'Possible damaged or intentional symbols. Compare original equation and fonts. Never replace automatically.',
                    [f'U+{ord(c):04X}' for c in candidates])
            breaks = [b for b in p.iter(tag('br')) if attr(b, 'type', 'textWrapping') == 'textWrapping']
            if breaks:
                jc = p.find('w:pPr/w:jc', NS)
                justified = jc is not None and attr(jc, 'val') in {'both','distribute','thaiDistribute'}
                code = 'JUSTIFIED_SOFT_BREAK' if justified else 'MANUAL_LINE_BREAK'
                add(code, part, where, 'Inspect Shift+Enter and effective alignment. A soft break can be intentional.')
            if 'Error! Reference source not found.' in text or 'Error! Bookmark not defined.' in text:
                add('FIELD_ERROR_TEXT', part, where, 'Check cross-reference targets and update permitted fields in Word.')

        for element in root.iter():
            local = element.tag.removeprefix('{' + W + '}')
            where = location(element)
            container = parent.get(element)
            if local == 'spacing' and container is not None:
                if container.tag == tag('rPr') and attr(element, 'val', '0') != '0':
                    add('CHARACTER_SPACING', part, where, 'Nondefault tracking setting. Compare with the approved style.', dict(element.attrib))
                if container.tag == tag('pPr'):
                    spacing_settings.append({'part':part, 'location':where,
                                             'properties':{k.rsplit('}',1)[-1]:v for k,v in element.attrib.items()}})
                    if attr(element, 'lineRule') == 'exact':
                        add('FIXED_LINE_HEIGHT', part, where, 'Exact line height can clip tall math or combining marks. Check the saved Word view.')
                    if any(attr(element, key).startswith('-') for key in ('before','after','line')):
                        add('NEGATIVE_SPACING', part, where, 'Inspect negative paragraph spacing against the template.')
            elif local == 'w' and attr(element,'val','100') != '100':
                add('TEXT_SCALE', part, where, 'Nondefault horizontal text scale. Do not compress text merely to meet a page limit.')
            elif local == 'position' and attr(element,'val','0') != '0':
                add('BASELINE_SHIFT', part, where, 'Inspect shifted baseline. Preserve intentional scientific notation.')
            elif local == 'jc' and attr(element,'val') in {'distribute','thaiDistribute'}:
                add('DISTRIBUTED_ALIGNMENT', part, where, 'Distributed alignment may stretch characters. Confirm template and language requirements.')
            elif local == 'keepNext' and enabled(element):
                add('KEEP_WITH_NEXT', part, where, 'Review chains of kept paragraphs. A heading or caption may legitimately need this setting.')
            elif local == 'trHeight' and attr(element,'hRule') == 'exact':
                add('EXACT_ROW_HEIGHT', part, where, 'Check table text for clipping inside a fixed-height row.')
            elif local == 'cantSplit' and enabled(element):
                add('UNSPLITTABLE_ROW', part, where, 'Check whether an unsplittable row causes a gap or exceeds usable page height.')
            elif local == 'vAlign' and attr(element,'val') in {'both','distribute'}:
                add('VERTICAL_JUSTIFICATION', part, where, 'Inspect section vertical alignment and unexpected vertical gaps.')
            elif local == 'type' and container is not None and container.tag == tag('sectPr') and attr(element,'val') in {'oddPage','evenPage'}:
                add('SECTION_START', part, where, 'Odd/even section starts can create intentional blank pages. Do not delete blindly.')
            elif local == 'altChunk':
                add('ALTCHUNK', part, where, 'Imported content requires native Word review. Do not flatten the document.')
            elif local == 'object':
                add('EMBEDDED_OBJECT', part, where, 'Preserve legacy equations and OLE objects. This tool does not open them.')
            elif local == 'rFonts':
                fonts.update(v for k,v in element.attrib.items() if k.rsplit('}',1)[-1] in {'ascii','hAnsi','eastAsia','cs'})
            elif local == 'font' and attr(element,'name'):
                fonts.add(attr(element,'name'))

        for group in root.iter():
            empty_count = 0
            for child in group:
                # A required final table paragraph is not flagged on its own.
                non_properties = [e for e in child if e.tag != tag('pPr')]
                empty = child.tag == tag('p') and not non_properties and child.find('.//w:sectPr',NS) is None
                empty_count = empty_count + 1 if empty else 0
                if empty_count == 2:
                    add('BLANK_PARAGRAPH_CHAIN', part, location(child), 'Inspect repeated empty paragraphs and anchors before deleting any.')

    with path.open('rb') as stream:
        source_hash = digest_stream(stream)
    if source_hash != initial_hash:
        raise ValueError('The source changed during inspection. Re-run against a stable copy.')
    return {'schema_version': 1, 'source_file': path.name, 'source_sha256': source_hash,
            'read_only': True, 'status': 'manual_review_required',
            'native_word_verified': False, 'pagination_verified': False,
            'rendering_verified': False, 'scientific_semantics_verified': False,
            'effective_styles_resolved': False,
            'coverage': 'Explicit XML settings and text candidates, including style definitions which may be unused. No full style inheritance, table-style cascade, font availability, glyph rendering, page geometry, or equation-to-code verification.',
            'inventory': inventory, 'declared_fonts': sorted(fonts),
            'paragraph_spacing_settings': spacing_settings,
            'part_sha256': part_hashes, 'findings': findings}


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('file', type=Path)
    parser.add_argument('--json', action='store_true')
    parser.add_argument('--fail-on-findings', action='store_true')
    args = parser.parse_args(argv)
    try:
        result = audit_docx(args.file)
    except (OSError, ValueError) as error:
        print(f'Inspection incomplete: {error}', file=sys.stderr)
        return 2
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        for row in result['findings']:
            print(f"{row['part']} {row['location']} {row['code']} {row['message']}")
        print(f"{len(result['findings'])} review candidate(s). No files changed. Native Word and visual checks remain unperformed.")
    return 1 if args.fail_on_findings and result['findings'] else 0


if __name__ == '__main__':
    sys.exit(main())
