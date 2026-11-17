"""Apply a hash-locked declarative source plan, with no network calls."""
import hashlib
import json
import lzma
from pathlib import Path
import subprocess

BASE = 'b9b5e01eceeda98e3ad6bdcc0744849b8c0bd509'
TREE = 'db691a51635c206e50a36421a4b0d0b5fc56a113'
DIGEST = '42543315349bc7b5008477e3b33df55f27c72d6cb2e1282bbeb946a681f37f46'
root = Path.cwd().resolve()
payload = b''.join((root / f'.release/plan.{i}').read_bytes() for i in range(4))
assert hashlib.sha256(payload).hexdigest() == DIGEST
plan = json.loads(lzma.decompress(payload).decode('utf-8'))
assert plan['base_commit'] == BASE and plan['expected_tree'] == TREE
assert len(plan['files']) == 41
subprocess.run(['git', 'checkout', '--detach', BASE], check=True)
paths = []
for entry in plan['files']:
    relative = entry['path']
    path = root / relative
    assert not Path(relative).is_absolute() and '..' not in Path(relative).parts
    assert path.resolve().is_relative_to(root) and not path.is_symlink()
    assert '.git' not in Path(relative).parts
    old = path.read_bytes() if path.exists() else b''
    if entry['old_sha256'] is None:
        assert not path.exists(), relative
    else:
        assert hashlib.sha256(old).hexdigest() == entry['old_sha256'], relative
    lines = old.decode('utf-8').splitlines(keepends=True)
    for edit in reversed(entry['edits']):
        lines[edit['start']:edit['end']] = edit['text'].splitlines(keepends=True)
    new = ''.join(lines).encode('utf-8')
    assert hashlib.sha256(new).hexdigest() == entry['new_sha256'], relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(new)
    paths.append(relative)
subprocess.run(['git', 'add', '--', *paths], check=True)
actual = subprocess.check_output(['git', 'write-tree'], text=True).strip()
assert actual == TREE, (actual, TREE)
subprocess.run(['git', 'diff', '--cached', '--check'], check=True)
print(f'Prepared exactly {len(paths)} files. Verified source tree {actual}.')
