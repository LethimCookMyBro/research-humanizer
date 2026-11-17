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


# Thresholds are editorial review triggers, not grammar rules or authorship tests.
PUNCTUATION_THRESHOLDS = {'commas_per_sentence': 3, 'asides_per_sentence': 2,
                          'and_per_sentence': 4, 'and_chain_min_words': 30}
MASK = '\ufff0'


def conceal(match: re.Match[str]) -> str:
    """Keep line positions and avoid creating punctuation-adjacent whitespace."""
    return ''.join('\n' if c == '\n' else MASK for c in match.group())


def mask_inline(text: str) -> str:
    """Protect common code/math and source syntax without hiding pending markers."""
    text = re.sub(r'(?<!`)(`+)(?!`).*?(?<!`)\1(?!`)', conceal, text)
    for pattern in (r'\\\(.*?\\\)', r'\$\$.*?\$\$',
                    r'(?<![\\$])\$(?!\$).*?(?<!\\)\$', r'\\\[.*?\\\]'):
        text = re.sub(pattern, conceal, text)
    # Link text remains prose; only targets are protected. Not a full Markdown parser.
    text = re.sub(r'!?\[([^\]]*)\]\([^\n]*?\)', lambda m: m[1], text)
    text = re.sub(r'(?:https?://|doi:)\S+', conceal, text, flags=re.I)
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
    text = re.sub(r'\b[\w.-]+\.(?:csv|py|json|md|txt|docx|pdf|tex|bib)\b', conceal, text, flags=re.I)
    text = re.sub(r'\b(?:v)?\d+(?:\.\d+){2,}\b', conceal, text)
    text = re.sub(r'(?<!\w)[+−-]?(?:\d+(?:[,.]\d+)*|\.\d+)(?:[eE][+-]?\d+)?', conceal, text)
    text = re.sub(r'\b(?:e\.g\.|i\.e\.|et al\.|Dr\.|Prof\.|Mr\.|Ms\.|Fig\.|Figs\.|Eq\.|Eqs\.|No\.|vs\.)', conceal, text)
    text = re.sub(r'\b(?:[A-Za-z]\.){2,}|\bPh\.D\.', conceal, text)
    text = re.sub(r'\b[A-Z]\.(?=\s*[A-Z])', conceal, text)
    return text


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
        clean = mask_numeric_context(raw)
        def add(rule: str, message: str, offset: int = 0) -> None:
            index = min(clean[:offset].count('\n'), len(block)-1)
            found.append({'line': block[index][0], 'end_line': block[-1][0],
                          'rule': rule, 'severity': 'review', 'message': message,
                          'excerpt': ' '.join(row[2].strip() for row in block[index:])[:180]})
        # Scan punctuation runs before treating periods as sentence boundaries.
        for match in re.finditer(r'\.{3,}|…|\.(?:\s+\.){2,}', clean):
            add('ELLIPSIS_REVIEW', 'Review an ellipsis in prose. Preserve documented omissions and mathematical sequences. Do not guess omitted text.', match.start())
        for match in re.finditer(r'(?<!\.)\.\.(?!\.)|[,，]{2,}|[!?！？]{2,}', clean):
            add('PUNCT_REPEAT_REVIEW', 'Review repeated punctuation. Keep literal strings and scientifically meaningful notation intact.', match.start())
        for match in re.finditer(r'\b[A-Za-z]{2,}\.\s+[A-Za-z]{2,}\.\s+[A-Za-z]{2,}\.(?=\s|$)',clean):
            add('FRAGMENT_CHAIN_REVIEW', 'Review isolated words separated by periods. Prefer a complete supported statement, not a mechanical short-sentence quota.', match.start())
        stack=[]; unbalanced=False
        for char in clean:
            if char=='(': stack.append(char)
            elif char==')':
                if stack: stack.pop()
                else: unbalanced=True
        if stack or unbalanced:
            add('PUNCT_UNBALANCED_REVIEW','Check unmatched prose parentheses against the source. Do not delete mathematical delimiters automatically.')
        for segment in re.finditer(r'[^.!?。！？]+(?:[.!?。！？]+|$)', clean):
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
        for match in re.finditer(r'(?<=\w)[,，](?=\w)|\w[ \t]+[,.!?]|(?<=[a-z])\.(?=[A-Z][a-z])',clean):
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
    findings: list[dict[str, Any]]=[]
    prose_lines: list[tuple[int, str, str]]=[]
    source_lines=text.splitlines()
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
        clean=mask_inline(line)
        if re.search(r'(?<!\\)(?:`|\$|\\\(|\\\[)',clean):
            add(number,'PARSE_UNCLOSED_INLINE','Check an unmatched supported delimiter. Escape literal currency markers. This region is not fully checked.',original,'incomplete')
        clean=re.sub(r'^(\s*(?:\*\*)?)Keywords:',r'\1Keywords',clean,count=1)
        prose_lines.append((number,clean,original))
        checks=((bool(re.search('[;；]', clean)),'PUNCT_SEMICOLON','Rewrite the prose semicolon.'),
                (bool(re.search('[:：]', clean)),'PUNCT_COLON','Review the prose colon. Keywords and reference entries are exempt.'),
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
    findings.extend(punctuation_findings(prose_lines))
    return sorted(findings,key=lambda item:item['line'])


def inspect_text(text: str) -> dict[str, Any]:
    findings=lint_text(text)
    incomplete=any(f['severity']=='incomplete' for f in findings)
    return {'status':'incomplete' if incomplete else 'needs_review' if findings else 'no_flags_in_checked_scope',
            'findings':findings,'authorship_detection':False,
            'punctuation_thresholds':dict(PUNCTUATION_THRESHOLDS),
            'checked':['supported prose punctuation','common contractions','pending markers','selected wording candidates','supported delimiter integrity','selected symbol contexts','selected contribution results','sentence-level punctuation review candidates'],
            'not_checked':['scientific_validity','grammar_correctness','all citation/quotation/notation forms','Thai sentence segmentation','semantic_equivalence','citation_support','full Markdown grammar','all Greek-symbol contexts','all contribution results','layout','anonymity','authorship']}


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
