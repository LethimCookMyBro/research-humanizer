#!/usr/bin/env python3
"""Read-only manuscript checks. Flags are review aids, never AI-authorship scores.

Supports common Markdown fences, YAML frontmatter, inline code, math and
reference headings. Malformed supported regions yield incomplete status.
This is not a complete Markdown/LaTeX parser. Exact quotations need review.
"""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import re
import sys
from typing import Any

CONTRACTIONS = re.compile(
    r"\b(?:[a-z]+n['’]t|(?:i|you|we|they|he|she|it|that|there|here|this|what|who|how|where|when|why)"
    r"['’](?:m|re|ve|ll|d|s)|let['’]s)\b", re.I)
PLACEHOLDERS = re.compile(
    r"\[(?:SOURCE REQUIRED|RESULT UNVERIFIED|AUTHOR DECISION|CITATION NEEDED|TBD|TODO)\]"
    r"|\{\{[^}\n]+\}\}", re.I)
REFERENCE_NAMES = {'references','bibliography','เอกสารอ้างอิง','บรรณานุกรม'}
SLOP = re.compile(
    r"\b(?:plays? a (?:crucial|pivotal|key) role|valuable insights|pav(?:e|es|ing) the way|"
    r"in (?:today['’]s |the )?(?:rapidly )?evolving landscape|groundbreaking framework|"
    r"revolutioniz\w*|a testament to|delve into|at its core)\b"
    r"|มีบทบาทสำคัญอย่างยิ่ง|เปิดมิติใหม่|พลิกโฉมวงการ|ในยุคที่เทคโนโลยีพัฒนาอย่างรวดเร็ว", re.I)


def mask_inline(text: str) -> str:
    """Protect common syntax; preserve labels and unmatched opening delimiters."""
    text = re.sub(r'(?<!`)(`+)(?!`).*?(?<!`)\1(?!`)', ' ', text)
    for pattern in (r'\\\(.*?\\\)', r'\$\$.*?\$\$',
                    r'(?<![\\$])\$(?!\$).*?(?<!\\)\$', r'\\\[.*?\\\]'):
        text = re.sub(pattern, ' ', text)
    text = re.sub(r'!?\[([^\]]*)\]\([^\n]*?\)', r'\1', text)
    return re.sub(r'(?:https?://|doi:)\S+', ' ', text, flags=re.I)


def lint_text(text: str) -> list[dict[str, Any]]:
    """Return findings without modifying the text. Retains the v2 list API."""
    findings: list[dict[str, Any]]=[]
    yaml_start=None; fence_state=None; math_state=None; reference_level=None; contribution_level=None
    def add(n, rule, message, original, severity='review'):
        findings.append({'line':n,'rule':rule,'severity':severity,
                         'message':message,'excerpt':original.strip()[:180]})
    for number, original in enumerate(text.splitlines(),1):
        line=original.lstrip('\ufeff') if number==1 else original
        stripped=line.strip()
        # Integrity checks MUST precede protected-syntax filtering.
        if PLACEHOLDERS.search(original):
            add(number,'DRAFT_PLACEHOLDER','Resolve the pending input before final delivery. Quoted examples need manual classification.',original,'required_fix')
        if '<!--' in original:
            add(number,'HIDDEN_COMMENT','Inspect hidden notes and identity information.',original)
        if number==1 and stripped=='---':
            yaml_start=number; continue
        if yaml_start is not None:
            if stripped in {'---','...'}: yaml_start=None
            continue
        fence=re.match(r'^\s*(`{3,}|~{3,})(.*)$',line)
        if fence_state is not None:
            char,length,_=fence_state
            if fence and fence[1][0]==char and len(fence[1])>=length and not fence[2].strip():
                fence_state=None
            continue
        if fence:
            fence_state=(fence[1][0],len(fence[1]),number); continue
        if math_state is not None:
            closing,_=math_state
            if closing not in line: continue
            line=line.split(closing,1)[1]; math_state=None
        for opening,closing in (('$$','$$'),(r'\[',r'\]')):
            if opening in line:
                prefix,suffix=line.split(opening,1)
                if closing not in suffix:
                    line=prefix; math_state=(closing,number); break
        heading=re.match(r'^\s*(#{1,6})\s+(.+?)\s*#*\s*$',line)
        if heading:
            level=len(heading[1])
            title=re.sub(r'^(?:\d+(?:\.\d+)*[.)]?|[IVXLCDM]+[.)])\s*','',heading[2]).strip().casefold()
            if reference_level is not None and level<=reference_level: reference_level=None
            if contribution_level is not None and level<=contribution_level: contribution_level=None
            if title in {'contributions','contribution','ผลงานหลัก','ผลงานวิจัยหลัก'}: contribution_level=level
            if title in REFERENCE_NAMES: reference_level=level; continue
        if reference_level is not None: continue
        if line.lstrip().startswith('>'):
            add(number,'QUOTATION_REVIEW','Verify exact quotation and source. Do not automatically rewrite it.',original); continue
        clean=mask_inline(line)
        if re.search(r'(?<!\\)(?:`|\$|\\\(|\\\[)',clean):
            add(number,'PARSE_UNCLOSED_INLINE','Check an unmatched supported delimiter. Escape literal currency markers. This region is not fully checked.',original,'incomplete')
        clean=re.sub(r'^(\s*(?:\*\*)?)Keywords:',r'\1Keywords',clean,count=1)
        checks=((';' in clean,'PUNCT_SEMICOLON','Rewrite the prose semicolon.'),
                (':' in clean,'PUNCT_COLON','Review the prose colon. Keywords and reference entries are exempt.'),
                (bool(re.search('[\u2013\u2014]',clean)),'PUNCT_LONG_DASH','Rewrite prose without long dashes.'),
                (bool(re.search(r'\s--\s',clean)),'PUNCT_DOUBLE_HYPHEN','Do not use double hyphens as prose separators.'),
                (bool(CONTRACTIONS.search(clean)),'CONTRACTION','Expand contractions. Preserve possessives and exact source strings.'))
        for matched,rule,message in checks:
            if matched: add(number,rule,message,original,'required_fix')
        if not line.lstrip().startswith('|'):
            for match in re.finditer('[\u0370-\u03ff\u1f00-\u1fff°±≤]',clean):
                around=clean[max(0,match.start()-8):match.end()+8]
                if not re.search(r'\d',around):
                    add(number,'SYMBOL_CONTEXT_REVIEW','Use the quantity name in prose. Verify whether this is legitimate numeric notation or an exact identifier before editing.',original)
                    break
        if contribution_level is not None and re.search(r'\b\d+(?:\.\d+)?\s*(?:%|ms\b|seconds?\b|minutes?\b|accuracy\b|percent\b|เปอร์เซ็นต์|วินาที)',clean,re.I):
            add(number,'CONTRIBUTION_RESULT','Move numerical performance results out of contribution bullets. Structural counts and identifiers need manual classification.',original,'required_fix')
        if SLOP.search(clean):
            add(number,'STYLE_CANDIDATE','Inspect for unsupported significance or generic filler. Context may justify the phrase. This is not evidence of AI authorship.',original)
    for state,rule in ((yaml_start,'PARSE_UNCLOSED_FRONTMATTER'),
                       (None if fence_state is None else fence_state[2],'PARSE_UNCLOSED_FENCE'),
                       (None if math_state is None else math_state[1],'PARSE_UNCLOSED_MATH')):
        if state is not None:
            add(state,rule,'Close or correct this protected region. Inspection is incomplete.','', 'incomplete')
    return sorted(findings,key=lambda item:item['line'])


def inspect_text(text: str) -> dict[str, Any]:
    findings=lint_text(text)
    incomplete=any(f['severity']=='incomplete' for f in findings)
    return {'status':'incomplete' if incomplete else 'needs_review' if findings else 'no_flags_in_checked_scope',
            'findings':findings,'authorship_detection':False,
            'checked':['supported prose punctuation','common contractions','pending markers','selected wording candidates','supported delimiter integrity','selected symbol contexts','selected contribution results'],
            'not_checked':['scientific_validity','semantic_equivalence','citation_support','full Markdown grammar','all Greek-symbol contexts','all contribution results','layout','anonymity','authorship']}


def main(argv=None) -> int:
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('files',nargs='+',type=Path)
    parser.add_argument('--json',action='store_true')
    parser.add_argument('--fail-on-findings',action='store_true')
    parser.add_argument('--fail-on-errors',action='store_true',help='Exit 1 for required fixes, not advisory wording candidates')
    args=parser.parse_args(argv); reports=[]
    for path in args.files:
        if path.suffix.lower() not in {'.md','.txt'}: parser.error('Use UTF-8 .md or .txt, not DOCX/PDF.')
        try: text=path.read_text(encoding='utf-8-sig')
        except (OSError,UnicodeError) as exc: parser.error(f'Cannot read {path}: {exc}')
        reports.append({'file':str(path),**inspect_text(text)})
    findings=[f for r in reports for f in r['findings']]
    if args.json:
        print(json.dumps({'schema_version':2,'heuristic_only':True,'total_findings':len(findings),'reports':reports},ensure_ascii=False,indent=2))
    else:
        for r in reports:
            for f in r['findings']: print(f"{r['file']}:{f['line']} {f['severity']} {f['rule']} {f['message']}")
        print(f'{len(findings)} finding(s). Manual review is required. No files changed.')
    if any(r['status']=='incomplete' for r in reports): return 2
    if args.fail_on_findings and findings: return 1
    if args.fail_on_errors and any(f['severity']=='required_fix' for f in findings): return 1
    return 0

if __name__=='__main__': sys.exit(main())
