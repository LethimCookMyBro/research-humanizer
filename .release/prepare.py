"""Apply one hash-locked, declarative release plan. No remote calls."""
import hashlib
import json
import lzma
from pathlib import Path
import subprocess

BASE = '21dfaf56da1f59fbd48d5810d8b867ec9a667cc1'
TREE = '1e6110eabc528d9685326986a567c6bc44be22a0'
PAYLOAD_SHA = '214d76cbe5975af53b4351e0f589865e2f994d79b0fb3d5adbc17b735c1aee5b'
root = Path.cwd().resolve()
payload = b''.join((root / f'.release/plan.{i}').read_bytes() for i in range(4))
assert hashlib.sha256(payload).hexdigest() == PAYLOAD_SHA, 'Payload checksum mismatch'
plan = json.loads(lzma.decompress(payload).decode('utf-8'))
assert plan['base_commit'] == BASE and plan['expected_tree'] == TREE
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
print(f'Prepared exactly {len(paths)} files. Verified tree {actual}.')
