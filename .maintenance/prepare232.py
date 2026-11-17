"""Apply the declared v2.3.2 patch on a pinned source and verify before upload."""
from pathlib import Path
import hashlib
import json
import lzma
import os
import re
import subprocess
import sys
import urllib.request

BASE='4f4e0297895cc2dad40811b7e7321a41010edc67'
REPO='LethimCookMyBro/research-humanizer'
EXPECTED_PAYLOAD='865dca00c222d78ad39f0f328b1811f97e53a606f4bc7f71a894410fc2efc12c'
root=Path.cwd().resolve()
payload=b''.join((root/f'.maintenance/v232.{i}').read_bytes() for i in range(2))
assert hashlib.sha256(payload).hexdigest()==EXPECTED_PAYLOAD
plan=json.loads(lzma.decompress(payload).decode('utf-8'))
assert plan['base']==BASE and plan['version']=='2.3.2'
subprocess.run(['git','checkout','--detach',BASE],check=True)
base_tree=subprocess.check_output(['git','rev-parse','HEAD^{tree}'],text=True).strip()
assert subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip()==BASE
S='skills/research-paper-craft/'
assert subprocess.check_output(['git','hash-object',S+'scripts/lint_manuscript.py'],text=True).strip()=='5ec1f7e45d5745dc4b46def8701da21bb50364bd'
changed=set()

def write(name,text):
    path=Path(name)
    assert not path.is_absolute() and '..' not in path.parts
    assert path.parts[0] not in {'.git','.github','.maintenance'}
    assert not path.is_symlink() and path.resolve().is_relative_to(root)
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(text,encoding='utf-8',newline='\n')
    changed.add(name)

def transform(name,fn):
    old=Path(name).read_text(encoding='utf-8')
    new=fn(old)
    assert new!=old, name+' did not change'
    write(name,new)

def run_tests(label,args,expected_failure=False):
    result=subprocess.run([sys.executable,'-B',*args],capture_output=True,text=True)
    output=result.stdout+result.stderr
    print('=== '+label+' ===',flush=True)
    print(output,flush=True)
    total=re.search(r'Ran (\d+) tests? in',output)
    assert total, label+' missing unittest count'
    failures=re.search(r'failures=(\d+)',output)
    errors=re.search(r'errors=(\d+)',output)
    if expected_failure:
        assert result.returncode!=0 and failures and not errors, label+' is not an expected assertion-only failure'
    else:
        assert result.returncode==0 and not errors and not failures,label+' failed'
    return {'suite':label,'tests':int(total[1]),'failures':int(failures[1]) if failures else 0,'errors':int(errors[1]) if errors else 0,'exit_code':result.returncode}

# Retain the original probe and demonstrate failures against the exact old linter.
for name in (S+'tests/test_text_integrity.py',S+'tests/fixtures/punctuation-v2.3.1-probes.json','tests/test_text_integrity_contract.py'):
    assert not Path(name).exists(),name
    write(name,plan['files'][name])
red_tools=run_tests('New tests on v2.3.1',['-m','unittest','discover','-s',S+'tests','-p','test_text_integrity.py','-v'],True)
red_contracts=run_tests('New documentation contracts before patch',['-m','unittest','discover','-s','tests','-p','test_text_integrity_contract.py','-v'],True)
assert red_tools['tests']==90 and red_tools['failures']==38

for name,text in plan['files'].items():
    if name!=S+'scripts/lint_manuscript.py' and name not in changed:
        assert not Path(name).exists(),name
    write(name,text)
for language in ('en','th'):
    transform(S+f'references/punctuation.{language}.md',lambda t,l=language:t+plan['append_'+l])
transform('VERSION',lambda t:'2.3.2\n' if t.strip()=='2.3.1' else t)
for name in ('.claude-plugin/plugin.json','.codex-plugin/plugin.json'):
    transform(name,lambda t:t.replace('"version": "2.3.1"','"version": "2.3.2"',1))
transform(S+'SKILL.md',lambda t:t.replace('version: "2.3.1"','version: "2.3.2"',1).replace(
    'Load punctuation review with writing. Check each drafted section and revision for overloaded clauses. Preserve notation and grammar. A threshold is not a quota.',
    'Load punctuation review with writing. Check each drafted section for clause load, quotation balance and suspicious Unicode. Preserve notation. A threshold is not a quota.'))
for name in ('site/index.html','site/th/index.html'):
    transform(name,lambda t:t.replace('2.3.1','2.3.2'))
for name in ('README.md','README(TH).md'):
    intro=('**2.3.2** closes the seven retained punctuation-probe misses and adds contextual quotation and Unicode checks. It preserves scientific notation and never rewrites inputs automatically. [Patch notes](docs/releases/v2.3.2.md) · [Executed checks](docs/VERIFICATION.md).\n\n'
           if name=='README.md' else '**2.3.2** เพิ่มการตรวจจุด อัญประกาศ และอักขระแฝงตามบริบท ครอบคลุมกรณีที่หลุดทั้งเจ็ดข้อจากการตรวจเดิม โดยรักษาสูตรและไม่แก้ไฟล์อัตโนมัติ [สิ่งที่แก้](docs/releases/v2.3.2.md) · [ผลตรวจ](docs/VERIFICATION.md)\n\n')
    def readme(t, intro=intro):
        t=t.replace('version-2.3.1-','version-2.3.2-')
        t=t.replace('Release v2.3.1','Release v2.3.2').replace('releases/tag/v2.3.1','releases/tag/v2.3.2')
        at=t.index('</div>')+len('</div>')
        return t[:at]+'\n\n'+intro+t[at:]
    transform(name,readme)
transform(S+'README.md',lambda t:t.replace('# Research Paper Craft 2.3.1','# Research Paper Craft 2.3.2',1)+'\n## Text integrity in 2.3.2\n\nThe same read-only lint command now checks the seven retained v2.3.1 misses and selected related forms. See the punctuation guide for quote balance, code-point diagnostics and protected contexts. Source-character warnings may appear inside protected source strings. They request comparison with the original, not deletion or normalization.\n')
for name in ('docs/KNOWN_ISSUES.md',S+'KNOWN_ISSUES.md'):
    transform(name,lambda t:t.replace('# Known limits in 2.3.1','# Known limits in 2.3.2',1)+'\n## Text-integrity coverage in 2.3.2\n\nThe seven misses in the retained 28-case v2.3.1 probe are now regression-tested. This does not close every possible punctuation or scientific-writing gap. Single-quote conventions, unusual multiline/nested quotations, unmarked dotted names, arbitrary fragment grammar and rendered missing-font boxes remain contextual/manual checks. All new warnings are review candidates. Thai word-break controls and legitimate script joins must not be globally removed. Source-character diagnostics may intentionally flag quoted literal replacement characters.\n')
transform('CHANGELOG.md',lambda t:t.replace('# Changelog\n','# Changelog\n\n## 2.3.2, 2026-11-17\n\n- Close seven retained punctuation-probe misses with contextual tests and preserve the original probe unchanged.\n- Add selected lowercase dot-spacing, fullwidth/small stop, multiword fragment, quotation-balance and source-character diagnostics.\n- Protect complete soft-wrapped quotes and common dotted technical forms. Expose invisible controls in reports without rewriting research inputs.\n- Keep source-bound writing, real-image requirements, ARS integration and Word-first safeguards. Expand bilingual review guidance and synchronize package/site versions.\n- Retain explicit grammar, rendered-glyph and live-model limitations.\n',1))
# A complete payload inventory is regenerated, not a partial list of changed files.
for p in Path(S).rglob('*.pyc'):
    raise AssertionError('Unexpected generated bytecode '+str(p))
checksums=''.join(hashlib.sha256(p.read_bytes()).hexdigest()+'  '+p.relative_to(Path(S)).as_posix()+'\n'
                  for p in sorted(Path(S).rglob('*')) if p.is_file() and p.name!='SHA256SUMS.txt')
write(S+'SHA256SUMS.txt',checksums)
commands=[('Repository and documentation',['-m','unittest','discover','-s','tests','-v']),
          ('Skill tools and contracts',['-m','unittest','discover','-s',S+'tests','-v']),
          ('Historical regressions',['docs/audit-v2.0/audit_regressions.py',S.rstrip('/')])]
results=[run_tests(label,args) for label,args in commands]
assert [r['tests'] for r in results]==[71,311,5]
record={'version':'2.3.2','base_commit':BASE,'baseline_linter_blob':'5ec1f7e45d5745dc4b46def8701da21bb50364bd',
        'execution':'GitHub Actions source preparation','source_preparation_run':os.environ.get('GITHUB_RUN_ID'),
        'python':sys.version.split()[0],'baseline_new_tests':red_tools,'baseline_new_contracts':red_contracts,
        'suites':results,'total_tests':sum(r['tests'] for r in results),'probe_cases':28,'repaired_probe_misses':7,
        'scope':'Software and static-contract tests with synthetic text. Not a model-quality or scientific-validity benchmark.',
        'not_performed':['live Claude/Codex/ARS run','native Word rendering','independent model-quality evaluation','universal grammar verification']}
write('docs/verification/release-v2.3.2.json',json.dumps(record,ensure_ascii=False,indent=2)+'\n')
summary='''## 2.3.2, 17 November 2026

Source preparation executed 71 repository/documentation tests, 311 skill tests and 5 historical regressions. All 387 passed. The 90 new tool tests first ran against the exact v2.3.1 linter and produced 38 assertion failures with no test errors. New documentation contracts also failed before the corresponding patch. After implementation the complete suites passed. The release workflow reruns them on the published commit.

The original 28-case public synthetic probe is retained byte-for-byte. All seven previously unflagged gap inputs now trigger their intended review diagnostics. Previously passing probe controls and existing detection expectations are preserved. Additional tests cover source positions, valid quotations across soft wraps, technical notation, multilingual controls, CLI return codes, unchanged input bytes and deterministic malformed-text cases. Test counts are not model-quality scores.

Only the selected syntax and patterns are covered. Unusual quotation conventions, arbitrary dotted identifiers, general grammar and rendered missing-font boxes still need review. No live host installation, ARS paper run, native Word check or independent model evaluation is claimed. Core evidence, figures, methods, full-paper guidance and the original Humanizer remain unchanged apart from the main routing sentence/version and the expanded punctuation guide.

[Executed record](verification/release-v2.3.2.json) · [Before/after probes](verification/punctuation-probes.v2.3.2.json) · [Patch notes](releases/v2.3.2.md)

'''
transform('docs/VERIFICATION.md',lambda t:t.replace('# Verification record\n','# Verification record\n\n'+summary,1))
# Verify the exact final source after writing its executed record.
final=[run_tests(label+' final',args) for label,args in commands]
assert [r['tests'] for r in final]==[71,311,5]
subprocess.run(['git','add','--',*sorted(changed)],check=True)
subprocess.run(['git','diff','--cached','--check'],check=True)
subprocess.run(['git','diff','--exit-code'],check=True)
names=subprocess.check_output(['git','diff','--cached','--name-only','-z']).decode().rstrip('\0').split('\0')
assert set(names)==changed
final_tree=subprocess.check_output(['git','write-tree'],text=True).strip()
print('FINAL_SOURCE_TREE='+final_tree,flush=True)
assert os.environ['GITHUB_REPOSITORY']==REPO
entries=[{'path':name,'mode':'100644','type':'blob','content':Path(name).read_text(encoding='utf-8')} for name in sorted(changed)]
body=json.dumps({'base_tree':base_tree,'tree':entries},ensure_ascii=False).encode()
request=urllib.request.Request(f'https://api.github.com/repos/{REPO}/git/trees',data=body,
    headers={'Authorization':'Bearer '+os.environ['GH_TOKEN'],'Accept':'application/vnd.github+json','Content-Type':'application/json'},method='POST')
with urllib.request.urlopen(request,timeout=90) as response:
    uploaded=json.load(response)
assert uploaded['sha']==final_tree
print('VERIFIED_RELEASE_TREE='+final_tree,flush=True)
print('CHANGED_FILES='+json.dumps(sorted(changed)),flush=True)
with open(os.environ['GITHUB_STEP_SUMMARY'],'a',encoding='utf-8') as out:
    out.write('## Verified v2.3.2 source\n\n387 full-suite checks passed. All seven retained probe misses are covered.\n\nTree `'+final_tree+'` uploaded without changing main or publishing a release.\n')
