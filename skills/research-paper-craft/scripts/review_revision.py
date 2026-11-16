#!/usr/bin/env python3
"""Read-only before/after review candidates, not a semantic-equivalence proof.

English and Thai phrase checks are deliberately partial. Reordered claims,
changed citation attachment and fluent paraphrases can evade these checks.
Use the claim ledger and human review even when no differences are flagged.
"""
from __future__ import annotations
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import re
import sys

PATTERNS={
 'NUMBER_CHANGED':r'(?<!\w)[+-]?\d+(?:[.,]\d+)*(?:[eE][+-]?\d+)?%?',
 'UNIT_CHANGED':r'\b(?:ms|s|sec|seconds?|minutes?|hours?|mm|cm|m|km|kg|mg|g|Hz|kHz|MHz|GB|MB|rad|radians?|degrees?)\b|°[CF]?|วินาที|นาที|ชั่วโมง|องศา',
 'CITATION_CHANGED':r'\[(?:\d+[ ,;–-]*)+\]|\[@[^\]]+\]|\\cite\w*\{[^}]+\}|\([^()\n]*\b\d{4}[a-z]?[^()\n]*\)',
 'MATH_CHANGED':r'\$\$[\s\S]*?\$\$|(?<![\\$])\$(?!\$)[^$]*?\$|\\\([\s\S]*?\\\)|\\\[[\s\S]*?\\\]',
 'NEGATION_CHANGED':r'\b(?:not|no|never|without|neither|cannot)\b|ไม่ได้|ไม่พบ|ไม่ใช่|ไม่|ปราศจาก',
 'SCOPE_CHANGED':r'\b(?:only|all|every|any|some|successful|excluded|included|within|under|except)\b|เฉพาะ|ทั้งหมด|ทุก|บาง|ภายใต้|ยกเว้น',
 'UNCERTAINTY_CHANGED':r'\b(?:may|might|could|suggests?|possibly|likely|demonstrates?|proves?|certainly)\b|อาจ|มีแนวโน้ม|ยืนยัน|พิสูจน์',
 'CAUSALITY_CHANGED':r'\b(?:associated|association|correlated|correlation|causes?|caused|causal|causality|leads? to)\b|สัมพันธ์|ส่งผลให้|ทำให้เกิด|เป็นสาเหตุ',
 'ESTIMAND_CHANGED':r'\b(?:mean|median|average|sum|weighted|unweighted|pooled|per-trial|per-participant)\b|ค่าเฉลี่ย|มัธยฐาน|ผลรวม|ถ่วงน้ำหนัก',
 'STATISTICAL_CLAIM_CHANGED':r'\b(?:statistically significant|not significant|no effect|equivalent|equivalence)\b|นัยสำคัญ|ไม่มีผล|เท่าเทียม',
}

def review(before: str, after: str, locked_terms=()) -> dict:
    if not isinstance(before,str) or not isinstance(after,str): raise ValueError('before and after must be strings')
    if not isinstance(locked_terms,(list,tuple)) or not all(isinstance(t,str) and t.strip() for t in locked_terms):
        raise ValueError('locked_terms must be a list of nonempty strings')
    findings=[]
    for rule,pattern in PATTERNS.items():
        a=Counter(re.findall(pattern,before,re.I)); b=Counter(re.findall(pattern,after,re.I))
        if a!=b:
            findings.append({'rule':rule,'severity':'review','removed':list((a-b).elements()),'added':list((b-a).elements()),
                             'message':'Compare the underlying claims. This difference may be valid; do not auto-rewrite.'})
    for term in locked_terms:
        # Exact phrase counts are intentional. A dropped/added occurrence can matter.
        if before.count(term)!=after.count(term):
            findings.append({'rule':'LOCKED_TERM_CHANGED','severity':'review','term':term,
                             'before_count':before.count(term),'after_count':after.count(term)})
    return {'schema_version':1,'unchanged':before==after,'status':'needs_review' if findings else 'no_flags_in_checked_scope',
            'semantic_equivalence':'not_established','authorship_detection':False,'findings':findings,
            'before_sha256':hashlib.sha256(before.encode()).hexdigest(),'after_sha256':hashlib.sha256(after.encode()).hexdigest(),
            'not_checked':['source_truth','claim_alignment','citation_attachment','full_semantics','author_voice','document_layout']}


def main(argv=None):
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('before',type=Path); p.add_argument('after',type=Path)
    p.add_argument('--terms',type=Path,help='JSON list of exact phrases to preserve')
    p.add_argument('--fail-on-findings',action='store_true')
    args=p.parse_args(argv)
    try:
        if any(x.suffix.lower() not in {'.md','.txt'} for x in (args.before,args.after)):
            raise ValueError('Use UTF-8 .md or .txt exports for analysis, never DOCX as text')
        terms=json.loads(args.terms.read_text(encoding='utf-8')) if args.terms else []
        result=review(args.before.read_text(encoding='utf-8-sig'),args.after.read_text(encoding='utf-8-sig'),terms)
    except (OSError,UnicodeError,ValueError) as exc: p.error(str(exc))
    print(json.dumps(result,ensure_ascii=False,indent=2))
    return 1 if args.fail_on_findings and result['findings'] else 0

if __name__=='__main__': sys.exit(main())
