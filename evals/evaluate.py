#!/usr/bin/env python3
"""Export research-writing evaluations and validate recorded responses.

Does not call a model, score authorship or claim an independent review.
"""
import argparse
import hashlib
import json
from pathlib import Path
import sys

ROOT=Path(__file__).resolve().parents[1]
CASES=Path(__file__).with_name('cases.jsonl')

def read_jsonl(path):
    rows=[]
    for n,line in enumerate(path.read_text(encoding='utf-8').splitlines(),1):
        if line.strip():
            row=json.loads(line)
            if not isinstance(row,dict): raise ValueError(f'{path}:{n} is not an object')
            rows.append(row)
    return rows

def jobs(cases, condition, skill_root):
    result=[]
    for c in cases:
        prompt='Revise or respond to this synthetic research task using only the supplied evidence.\n'
        if condition=='skill':
            prompt+=(skill_root/'SKILL.md').read_text(encoding='utf-8')+'\n'
            prompt+=(skill_root/f"references/{c['topic']}.{c['language']}.md").read_text(encoding='utf-8')+'\n'
        prompt+=f"\nSource note\n{c['source']}\n\nDraft\n{c['draft']}\n\nTask\n{c['task']}\n"
        result.append({'case_id':c['id'],'condition':condition,'prompt':prompt,
                       'prompt_sha256':hashlib.sha256(prompt.encode()).hexdigest()})
    return result

def check(jobs, responses):
    expected={j['case_id']:j for j in jobs}; seen=set(); errors=[]
    if not jobs: errors.append('No jobs supplied')
    if len(expected)!=len(jobs): errors.append('Duplicate job IDs')
    for row in responses:
        cid=row.get('case_id')
        if not isinstance(cid,str): errors.append('case_id must be a string'); continue
        if cid in seen: errors.append(f'{cid}: duplicate response')
        seen.add(cid)
        if cid not in expected: errors.append(f'{cid}: unknown case'); continue
        for key in ('model','host','run_id','executed_at','prompt_sha256','response'):
            if not isinstance(row.get(key),str) or not row[key].strip(): errors.append(f'{cid}: missing {key}')
        if row.get('prompt_sha256')!=expected[cid]['prompt_sha256']: errors.append(f'{cid}: prompt hash mismatch')
    for cid in sorted(set(expected)-seen): errors.append(f'{cid}: response missing')
    return {'record_status':'invalid' if errors else 'complete_records', 'errors':errors,
            'case_count':len(expected),'response_count':len(responses),
            'model_execution':'declared_not_independently_verified','human_review':'not_rated',
            'quality_improvement':'not_established'}

def main(argv=None):
    p=argparse.ArgumentParser(description=__doc__); sub=p.add_subparsers(dest='command',required=True)
    export=sub.add_parser('export'); export.add_argument('--condition',choices=['baseline','skill'],required=True)
    export.add_argument('--skill-root',type=Path,default=ROOT/'skills/research-paper-craft'); export.add_argument('--out',type=Path,required=True)
    verify=sub.add_parser('check'); verify.add_argument('--jobs',type=Path,required=True); verify.add_argument('--responses',type=Path,required=True)
    args=p.parse_args(argv)
    try:
        if args.command=='export':
            output=jobs(read_jsonl(CASES),args.condition,args.skill_root)
            # Exclusive creation prevents accidentally overwriting recorded runs.
            with args.out.open('x',encoding='utf-8') as f:
                for row in output: f.write(json.dumps(row,ensure_ascii=False)+'\n')
            print(f'Exported {len(output)} prompts. No model was called.'); return 0
        result=check(read_jsonl(args.jobs),read_jsonl(args.responses))
    except (OSError,UnicodeError,ValueError,KeyError,TypeError) as exc: p.error(str(exc))
    print(json.dumps(result,ensure_ascii=False,indent=2)); return 1 if result['errors'] else 0

if __name__=='__main__': sys.exit(main())
