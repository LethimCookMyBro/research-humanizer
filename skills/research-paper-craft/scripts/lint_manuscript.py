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
import unicodedata
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


# Thresholds are editorial review triggers, not grammar rules or authorship tests.
PUNCTUATION_THRESHOLDS = {'commas_per_sentence': 3, 'asides_per_sentence': 2,
                          'and_per_sentence': 4, 'and_chain_min_words': 30}
MASK = '\ufff0'


def conceal(match: re.Match[str]) -> str:
    """Keep line positions and avoid creating punctuation-adjacent whitespace."""
    return ''.join('\n' if c == '\n' else MASK for c in match.group())


def mask_inline(text: str, protect_quotes: bool = True) -> str:
    """Protect common code/math and source syntax without hiding pending markers."""
    text = re.sub(r'(?<!`)(`+)(?!`).*?(?<!`)\1(?!`)', conceal, text)
    for pattern in (r'\\\(.*?\\\)', r'\$\$.*?\$\$',
                    r'(?<![\\$])\$(?!\$).*?(?<!\\)\$', r'\\\[.*?\\\]'):
        text = re.sub(pattern, conceal, text)
    # Link text remains prose; only targets are protected. Not a full Markdown parser.
    text = re.sub(r'!?\[([^\]]*)\]\([^\n]*?\)',
                  lambda m: MASK * (m.start(1)-m.start()) + m[1] + MASK * (m.end()-m.end(1)), text)
    text = re.sub(r'(?:https?://|doi:)[^\s"“”«»「」『』<>]+', conceal, text, flags=re.I)
    if protect_quotes:
        for pattern in (r'"(?:\\.|[^"\\])*"', r'“[^”]*”', r'«[^»]*»'):
            text = re.sub(pattern, conceal, text)
    text = re.sub(r'\[\d+(?:\s*[,;–-]\s*\d+)*\]', conceal, text)
    text = re.sub(r'\[\^[^\]\n]+\]', conceal, text)
    text = re.sub(r'\[[^\]\n]*@[A-Za-z0-9_][^\]\n]*\]', conceal, text)
    text = re.sub(r'\\cite\w*\*?(?:\[[^\]\n]*\])*\{[^}\n]*\}', conceal, text)
    # Recognize ordinary parenthetical author-year citations, not their truth.
    author = r"[A-Z][A-Za-z'’.-]*(?:\s+(?:et al\.?|and\s+[A-Z][A-Za-z'’.-]*|&\s+[A-Z][A-Za-z'’.-]*))?"
    cite = author + r',?\s+(?:19|20)\d{2}[a-z]?(?:,\s*(?:p|pp)\.\s*\d+(?:[-–]\d+)?)?'
    text = re.sub(r'\(' + cite + r'(?:;\s*' + cite + r')*\)', conceal, text)
    text = re.sub(r'\b\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?(?:Z|[+-]\d{2}:\d{2})\b', conceal, text)
    text = re.sub(r'\b\d+(?:\.\d+)?(?::\d+(?:\.\d+)?)+\b', conceal, text)
    text = re.sub(r'(?:[A-Za-z]:[\\/]|\.{1,2}/)[^\s]+', conceal, text)
    text = re.sub(r'^\s*\[[^\]\n]+\]:\s*\S+.*$', conceal, text)
    text = re.sub(r'(?<!\w)[+−-]?\d+(?:\.\d+)?\s*–\s*[+−-]?\d+(?:\.\d+)?', conceal, text)
    return text


def mask_numeric_context(text: str) -> str:
    """Conservative punctuation-only exclusions. Never used to rewrite inputs."""
    atom = r'(?:[A-Za-z\u0370-\u03ff](?:_\w+)?|[+−-]?(?:\d+(?:\.\d+)?|\.\d+))'
    formula = r'(?<!\w)' + atom + r'(?:\s*(?:[=+−*/<>-]|[<>]=|≤|≥)\s*' + atom + r')+(?!\w)'
    text = re.sub(formula, conceal, text)
    # Tests/statistics and mathematical grouping are not explanatory asides.
    text = re.sub(r'\b(?:t|F|r|chi2)\(\s*\d+(?:\s*,\s*\d+)*\s*\)\s*=\s*[+-]?(?:\d+(?:\.\d+)?|\.\d+)', conceal, text)
    text = re.sub(r'\(\s*'+atom+r'(?:\s*,\s*'+atom+r')*\s*\)', conceal, text)
    text = re.sub(r'\(\s*[A-Z][A-Z0-9-]{1,12}\s*\)', conceal, text)
    text = re.sub(r'\((?:Eq\.?|Fig\.?|Section)\s+\d+(?:\.\d+)*\)', conceal, text, flags=re.I)
    text = re.sub(r'\b(?:kg|mg|g|km|cm|mm|m|ms|s|mol|mL|L|J|N|Pa)/(?:kg|g|ms|s|mL|L|mol|min|h)\b', conceal, text)
    text = re.sub(r'(?:[A-Za-z]:[\\/]|\.{1,2}/)[^\s]+', conceal, text)
    text = re.sub(r'\b[\w.-]+\.(?:csv|py|json|md|txt|docx|pdf|tex|bib|png|jpg|jpeg|svg|tif|tiff|webp|xlsx|xls|pptx|ipynb|npy|npz|zip|gz|yaml|yml|toml|ini|html|xml|log|dat|bin)\b', conceal, text, flags=re.I)
    text = re.sub(r'\b(?:v)?\d+(?:\.\d+){2,}\b', conceal, text)
    text = re.sub(r'(?<!\w)[+−-]?(?:\d+(?:[,.]\d+)*|\.\d+)(?:[eE][+-]?\d+)?', conceal, text)
    text = re.sub(r'\b(?:e\.g\.|i\.e\.|et al\.|Dr\.|Prof\.|Mr\.|Ms\.|Fig\.|Figs\.|Eq\.|Eqs\.|No\.|vs\.)', conceal, text)
    text = re.sub(r'\b(?:[A-Za-z]\.){2,}|\bPh\.D\.', conceal, text)
    text = re.sub(r'\b[A-Z]\.(?=\s*[A-Z])', conceal, text)
    return text


# Integrity diagnostics never normalize source Unicode or propose missing glyphs.
_INVISIBLE = {'\u00ad', '\u200b', '\u200c', '\u200d', '\u2060', '\ufeff'}
_BIDI = {chr(n) for n in (*range(0x202a, 0x202f), *range(0x2066, 0x206a), 0x061c, 0x200e, 0x200f)}
_QUOTE_PAIRS = {'"': '"', '“': '”', '«': '»', '「': '」', '『': '』'}


def safe_excerpt(text: str) -> str:
    """Escape invisible controls in reports only. Manuscript bytes stay intact."""
    return ''.join(f'\\u{ord(c):04x}' if c in _INVISIBLE | _BIDI or
                   (unicodedata.category(c) == 'Cc' and c not in '\n\t\r') else c
                   for c in text)


def character_findings(text: str) -> list[dict[str, Any]]:
    """Inspect source characters even where a style pass protects quotations/code.

    Replacement and directional controls require contextual review. An invisible
    Latin-word interruption is suspicious; Thai word boundaries and script joins
    are not classified as defects. This is not a rendered-font or encoding repair.
    """
    result = []
    for number, line in enumerate(text.splitlines(keepends=True), 1):
        seen = set()
        for index, char in enumerate(line):
            rule = None
            if char in {'\ufffd', '\ufffc'}:
                rule = 'UNICODE_REPLACEMENT_REVIEW'
                reason = 'Compare the original export/encoding. A literal character may be intentional. Do not guess or replace it.'
            elif char in _BIDI:
                rule = 'BIDI_CONTROL_REVIEW'
                reason = 'Check intended text direction and source. This control can be legitimate in multilingual text. Do not strip it blindly.'
            elif char == '\ufeff' and not (number == 1 and index == 0):
                rule = 'INVISIBLE_CHARACTER_REVIEW'
                reason = 'Review an internal BOM/word-joining character against the original. Do not normalize the whole document.'
            elif char in _INVISIBLE:
                left = line[index-1] if index else ''
                right = line[index+1] if index+1 < len(line) else ''
                if re.fullmatch(r'[A-Za-z0-9]', left) and re.fullmatch(r'[A-Za-z0-9]', right):
                    rule = 'INVISIBLE_CHARACTER_REVIEW'
                    reason = 'Review a format character inside a Latin word or number. Preserve intentional shaping, hyphenation and line-break control.'
            elif unicodedata.category(char) == 'Cc' and char not in '\t\n\r':
                rule = 'CONTROL_CHARACTER_REVIEW'
                reason = 'Inspect the source/export for an unexpected control character. Do not silently discard source data.'
            if rule and (rule, char) not in seen:
                seen.add((rule, char))
                point = f'U+{ord(char):04X}'
                name = unicodedata.name(char, 'CONTROL CHARACTER')
                result.append({'line': number, 'column': index+1, 'rule': rule,
                               'severity': 'review', 'codepoint': point,
                               'message': f'{point} {name}. {reason}',
                               'excerpt': safe_excerpt(line.strip())[:180]})
    return result


def quote_context(lines: list[tuple[int, str, str]]) -> tuple[list[tuple[int, str, str]], list[dict[str, Any]]]:
    """Mask complete supported quotes over soft wraps; report unmatched marks.

    Do not infer repairs, hide unclosed tails or pair across blank paragraphs,
    omitted code/reference regions, separate list items, headings or table rows.
    ASCII apostrophes and primes are deliberately not treated as quote openers.
    """
    output = []
    findings = []
    block = []

    def flush() -> None:
        if not block:
            return
        text = '\n'.join(row[1] for row in block)
        masked = list(text)
        stack = []
        pairs = []
        unmatched = []
        for i, char in enumerate(text):
            if char not in set(_QUOTE_PAIRS) | set(_QUOTE_PAIRS.values()):
                continue
            j = i-1
            while j >= 0 and text[j] == '\\':
                j -= 1
            if (i-1-j) % 2:
                continue
            if stack and char == _QUOTE_PAIRS[stack[-1][0]]:
                _, start = stack.pop()
                pairs.append((start, i+1))
            elif char == '"' and i and text[i-1].isdigit() and not any(q == '"' for q, _ in stack):
                # Common inch mark. Mathematical prime syntax needs manual review.
                continue
            elif char in _QUOTE_PAIRS:
                stack.append((char, i))
            else:
                unmatched.append(i)
        unmatched.extend(index for _, index in stack)
        for start, end in pairs:
            for i in range(start, end):
                if masked[i] != '\n':
                    masked[i] = MASK
        for offset in sorted(set(unmatched)):
            row = text[:offset].count('\n')
            column = offset-text.rfind('\n', 0, offset)
            findings.append({'line': block[row][0], 'column': column,
                             'rule': 'QUOTE_BALANCE_REVIEW', 'severity': 'review',
                             'message': 'Review an unmatched supported quotation mark against the source. Escapes, inch/prime marks and language conventions matter. No quoted wording is repaired automatically.',
                             'excerpt': safe_excerpt(block[row][2].strip())[:180]})
        for row, clean in zip(block, ''.join(masked).split('\n')):
            output.append((row[0], clean, row[2]))
        block.clear()

    for row in lines:
        number, clean, _ = row
        structural = bool(re.match(r'^\s*(?:#{1,6}\s|[-+*]\s|\d+[.)]\s|\|)', clean))
        if block and (number != block[-1][0]+1 or not clean.strip() or structural):
            flush()
        if not clean.strip():
            output.append(row)
            continue
        block.append(row)
        if re.match(r'^\s*(?:#{1,6}\s|\|)', clean):
            flush()
    flush()
    return output, findings


def mask_dotted_tokens(text: str) -> str:
    """Recognize common addresses and function calls, not arbitrary identifiers."""
    patterns = (
        r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b',
        r'\b(?:[A-Za-z0-9-]+\.)+(?:com|org|net|edu|gov|io|ai|dev|app|local)\b(?:/[^\s]*)?',
        r'\bwww\.[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b(?:/[^\s]*)?',
        r'\b[A-Za-z_]\w*(?:\.[A-Za-z_]\w*)+(?=\()',
    )
    for pattern in patterns:
        text = re.sub(pattern, conceal, text)
    return text


def phrase_fragment_offsets(text: str) -> list[int]:
    """Selected short adjective/noun patterns only; not a clause parser."""
    atom = (r'(?:[A-Za-z]{2,}|'
            r'(?:Very|Highly|Extremely|Quite|Remarkably)\s+'
            r'(?:fast|clear|effective|efficient|robust|accurate|reliable|simple|useful)|'
            r'(?:Low|High|Minimal|Rapid|Clear|Strong)\s+'
            r'(?:cost|accuracy|feedback|latency|overhead|performance|support))')
    pattern = r'(?<![\w.])'+atom+r'\.\s+'+atom+r'\.\s+'+atom+r'\.(?=\s|$)'
    return [m.start() for m in re.finditer(pattern, text, re.I)]


def punctuation_findings(lines: list[tuple[int, str, str]]) -> list[dict[str, Any]]:
    """Review approximate sentences, joining soft-wrapped prose but not paragraphs.

    Recognized lists, headings, tables and protected regions are boundaries.
    Threshold crossings are advisory. This does not parse grammatical clauses.
    """
    found: list[dict[str, Any]] = []
    block: list[tuple[int, str, str]] = []

    def flush() -> None:
        if not block:
            return
        raw = '\n'.join(row[1] for row in block)
        clean = mask_dotted_tokens(mask_numeric_context(raw))
        def add(rule: str, message: str, offset: int = 0) -> None:
            index = min(clean[:offset].count('\n'), len(block)-1)
            found.append({'line': block[index][0], 'end_line': block[-1][0],
                          'rule': rule, 'severity': 'review', 'message': message,
                          'excerpt': ' '.join(row[2].strip() for row in block[index:])[:180]})
        # Scan punctuation runs before treating periods as sentence boundaries.
        for match in re.finditer(r'[.．﹒]{3,}|…|[.．﹒](?:\s+[.．﹒]){2,}', clean):
            add('ELLIPSIS_REVIEW', 'Review an ellipsis in prose. Preserve documented omissions and mathematical sequences. Do not guess omitted text.', match.start())
        for match in re.finditer(r'(?<![.．﹒])[.．﹒]{2}(?![.．﹒])|。{2,}|[,，]{2,}|[!?！？]{2,}', clean):
            add('PUNCT_REPEAT_REVIEW', 'Review repeated punctuation. Keep literal strings and scientifically meaningful notation intact.', match.start())
        for offset in phrase_fragment_offsets(clean):
            add('FRAGMENT_CHAIN_REVIEW', 'Review a run of short word/phrase fragments. Labels or quoted examples may be intentional. Do not impose a short-sentence quota or invent a missing claim.', offset)
        for match in re.finditer(r'[A-Za-z][．﹒]', clean):
            add('PUNCT_WIDTH_REVIEW', 'Check a fullwidth or small full stop in Latin prose against the target language and source. Do not normalize all Unicode punctuation.', match.end()-1)
        for match in re.finditer('[□◻]', raw):
            add('GLYPH_CONTEXT_REVIEW', 'Check whether this literal square is intentional notation or a damaged export. A text scan cannot see missing-font glyphs. Compare the original and never guess a replacement.', match.start())
        stack=[]; unbalanced=False
        for char in clean:
            if char=='(': stack.append(char)
            elif char==')':
                if stack: stack.pop()
                else: unbalanced=True
        if stack or unbalanced:
            add('PUNCT_UNBALANCED_REVIEW','Check unmatched prose parentheses against the source. Do not delete mathematical delimiters automatically.')
        for segment in re.finditer(r'[^.!?。！？．﹒]+(?:[.!?。！？．﹒]+|$)', clean):
            sent=segment.group(); offset=segment.start()+len(sent)-len(sent.lstrip())
            if sum(sent.count(c) for c in ',，') >= PUNCTUATION_THRESHOLDS['commas_per_sentence']:
                add('COMMA_DENSITY_REVIEW','Three or more prose commas in an approximate sentence. Review clause load and split by meaning when useful. Preserve grammar, scope and genuine lists. This is not a comma ban.',offset)
            if re.search(r'\w[^\n]*,\s*(?:however|therefore|nevertheless|consequently|thus|instead)\s*,',sent,re.I):
                add('CLAUSE_LINK_REVIEW','Inspect the relationship between clauses. Do not repair a possible comma splice by blindly deleting punctuation or adding and.',offset)
            if re.search(r'\S\s+-\s+\S',sent):
                add('PUNCT_SPACED_HYPHEN','Review a spaced hyphen used as a prose separator. Preserve subtraction, negative signs, ranges and lexical hyphens.',offset)
            if re.search(r'[=+&→⇒↔]|->|=>',sent):
                add('PROSE_OPERATOR_REVIEW','Review symbolic shorthand in prose. State the relationship in words when appropriate. Preserve genuine equations, names, diagram relations and definitions.',offset)
            if re.search(r'[^\W\d_]+\s*/\s*[^\W\d_]+',sent,re.UNICODE):
                add('SLASH_SHORTHAND_REVIEW','Review slash shorthand for its intended relationship. Do not choose and or or without evidence. Preserve units, ratios, paths and defined labels.',offset)
            if sent.count('(') >= PUNCTUATION_THRESHOLDS['asides_per_sentence']:
                add('PARENTHETICAL_LOAD_REVIEW','Review repeated or nested explanatory parentheses. Preserve citations, abbreviations and mathematical grouping.',offset)
            if (len(re.findall(r'\band\b',sent,re.I)) >= PUNCTUATION_THRESHOLDS['and_per_sentence']
                    and len(re.findall(r"\b[A-Za-z]+(?:['’][A-Za-z]+)?\b",sent)) >= PUNCTUATION_THRESHOLDS['and_chain_min_words']):
                add('CONJUNCTION_CHAIN_REVIEW','Review a long and-chain. Splitting by scientific role is preferable to replacing every comma with and.',offset)
        for match in re.finditer(r'(?<=\w)[,，](?=\w)|\w[ \t]+[,.!?]|(?<=[a-z])\.(?=[A-Za-z]{2,})',clean):
            add('PUNCT_SPACING_REVIEW','Review punctuation spacing in prose. Preserve decimal marks, source strings, language conventions and intentional notation.',match.start())
        block.clear()

    for number,clean,original in lines:
        stripped=clean.strip()
        if block and number != block[-1][0]+1:
            flush()
        if not stripped or stripped.startswith('|'):
            flush(); continue
        if re.match(r'^\s*#{1,6}\s',clean):
            flush(); block.append((number,clean,original)); flush(); continue
        if re.match(r'^\s*(?:[-+*]\s|\d+[.)]\s)',clean):
            flush(); block.append((number,clean,original)); continue
        block.append((number,clean,original))
    flush()
    return found


def lint_text(text: str) -> list[dict[str, Any]]:
    """Return findings without modifying the text. Retains the v2 list API."""
    findings: list[dict[str, Any]]=character_findings(text)
    prose_lines: list[tuple[int, str, str]]=[]
    source_lines=text.splitlines()
    contribution_lines=set()
    yaml_start=None; fence_state=None; math_state=None; reference_level=None; contribution_level=None
    def add(n, rule, message, original, severity='review'):
        findings.append({'line':n,'rule':rule,'severity':severity,
                         'message':message,'excerpt':original.strip()[:180]})
    for number, original in enumerate(source_lines,1):
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
        if re.fullmatch(r"\s*(?:={3,}|(?:-\s*){3,}|(?:\*\s*){3,}|(?:_\s*){3,})\s*",line):
            previous=source_lines[number-2].strip() if number>1 else ''
            setext=bool(previous and re.fullmatch(r'[-=]+',stripped))
            if not setext:
                add(number,'DECORATIVE_SEPARATOR_REVIEW','Review a standalone decorative separator. Preserve Markdown heading syntax and required template rules.',original)
            continue
        if line.lstrip().startswith('>'):
            add(number,'QUOTATION_REVIEW','Verify exact quotation and source. Do not automatically rewrite it.',original); continue
        prose_lines.append((number, mask_inline(line, protect_quotes=False), original))
        if contribution_level is not None:
            contribution_lines.add(number)
    prose_lines, quote_flags = quote_context(prose_lines)
    findings.extend(quote_flags)
    for number, clean, original in prose_lines:
        if re.search(r'(?<!\\)(?:`|\$|\\\(|\\\[)',clean):
            add(number,'PARSE_UNCLOSED_INLINE','Check an unmatched supported delimiter. Escape literal currency markers. This region is not fully checked.',original,'incomplete')
        clean=re.sub(r'^(\s*(?:\*\*)?)Keywords:',r'\1Keywords',clean,count=1)
        checks=((bool(re.search('[;；]', clean)),'PUNCT_SEMICOLON','Rewrite the prose semicolon.'),
                (bool(re.search('[:：]', clean)),'PUNCT_COLON','Review the prose colon. Keywords and reference entries are exempt.'),
                (bool(re.search('[\u2013\u2014]',clean)),'PUNCT_LONG_DASH','Rewrite prose without long dashes.'),
                (bool(re.search(r'\s--\s',clean)),'PUNCT_DOUBLE_HYPHEN','Do not use double hyphens as prose separators.'),
                (bool(CONTRACTIONS.search(clean)),'CONTRACTION','Expand contractions. Preserve possessives and exact source strings.'))
        for matched,rule,message in checks:
            if matched: add(number,rule,message,original,'required_fix')
        if not original.lstrip().startswith('|'):
            for match in re.finditer('[\u0370-\u03ff\u1f00-\u1fff°±≤]',clean):
                around=clean[max(0,match.start()-8):match.end()+8]
                if not re.search(r'\d',around):
                    add(number,'SYMBOL_CONTEXT_REVIEW','Use the quantity name in prose. Verify whether this is legitimate numeric notation or an exact identifier before editing.',original)
                    break
        if number in contribution_lines and re.search(r'\b\d+(?:\.\d+)?\s*(?:%|ms\b|seconds?\b|minutes?\b|accuracy\b|percent\b|เปอร์เซ็นต์|วินาที)',clean,re.I):
            add(number,'CONTRIBUTION_RESULT','Move numerical performance results out of contribution bullets. Structural counts and identifiers need manual classification.',original,'required_fix')
        if SLOP.search(clean):
            add(number,'STYLE_CANDIDATE','Inspect for unsupported significance or generic filler. Context may justify the phrase. This is not evidence of AI authorship.',original)
    for state,rule in ((yaml_start,'PARSE_UNCLOSED_FRONTMATTER'),
                       (None if fence_state is None else fence_state[2],'PARSE_UNCLOSED_FENCE'),
                       (None if math_state is None else math_state[1],'PARSE_UNCLOSED_MATH')):
        if state is not None:
            add(state,rule,'Close or correct this protected region. Inspection is incomplete.','', 'incomplete')
    findings.extend(punctuation_findings(prose_lines))
    for finding in findings:
        finding['excerpt'] = safe_excerpt(finding['excerpt'])[:180]
    return sorted(findings,key=lambda item:item['line'])


def inspect_text(text: str) -> dict[str, Any]:
    findings=lint_text(text)
    incomplete=any(f['severity']=='incomplete' for f in findings)
    return {'status':'incomplete' if incomplete else 'needs_review' if findings else 'no_flags_in_checked_scope',
            'findings':findings,'authorship_detection':False,
            'punctuation_thresholds':dict(PUNCTUATION_THRESHOLDS),
            'checked':['supported prose punctuation','common contractions','pending markers','selected wording candidates','supported delimiter integrity','selected symbol contexts','selected contribution results','sentence-level punctuation review candidates','selected quote balance','selected source-character integrity'],
            'not_checked':['scientific_validity','grammar_correctness','all citation/quotation/notation forms','Thai sentence segmentation','semantic_equivalence','citation_support','full Markdown grammar','all Greek-symbol contexts','all contribution results','rendered glyph appearance','all dotted identifiers','all fragment patterns','layout','anonymity','authorship']}


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
