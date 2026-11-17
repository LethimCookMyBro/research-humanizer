"""Apply a checksum-locked source patch in an isolated Actions checkout."""
import hashlib
import json
import lzma
from pathlib import Path
import subprocess

BASE = 'bedb58e290b4dc6365c47be669927d6c94246977'
BASE_TREE = '64b2c0c689f6e043cebc41fe3ba0b8cddedc6414'
PAYLOAD_SHA = '7b280da6f82c6d8594b79126b20dc0ae7a54fac2aa9caf9b647e8c485b42ebbb'
root = Path.cwd().resolve()
payload = b''.join((root / f'.maintenance/punctuation-plan.{i}').read_bytes() for i in range(2))
assert hashlib.sha256(payload).hexdigest() == PAYLOAD_SHA, 'Payload checksum mismatch'
plan = json.loads(lzma.decompress(payload).decode('utf-8'))
assert plan['base'] == BASE and plan['base_tree'] == BASE_TREE
assert len(plan['files']) == 21 and len(plan['transforms']) == 4
subprocess.run(['git', 'checkout', '--detach', BASE], check=True)
assert subprocess.check_output(['git', 'rev-parse', 'HEAD^{tree}'], text=True).strip() == BASE_TREE

def blob(raw):
    return hashlib.sha1(b'blob ' + str(len(raw)).encode() + b'\0' + raw).hexdigest()

def checked_path(entry):
    rel = entry['path']
    path = root / rel
    assert not Path(rel).is_absolute() and '..' not in Path(rel).parts
    assert '.git' not in Path(rel).parts and not rel.startswith('.github/')
    assert path.resolve().is_relative_to(root) and not path.is_symlink()
    before = path.read_bytes() if path.exists() else b''
    if entry['before_blob'] is None:
        assert not path.exists(), rel
    else:
        assert blob(before) == entry['before_blob'], rel
    return path, before

paths = []
for entry in plan['files']:
    path, before = checked_path(entry)
    lines = before.decode('utf-8').splitlines(keepends=True)
    for edit in reversed(entry['edits']):
        assert 0 <= edit['start'] <= edit['end'] <= len(lines)
        lines[edit['start']:edit['end']] = edit['text'].splitlines(keepends=True)
    raw = ''.join(lines).encode('utf-8')
    assert blob(raw) == entry['after_blob'], entry['path']
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(raw)
    paths.append(entry['path'])
for entry in plan['transforms']:
    path, before = checked_path(entry)
    text = before.decode('utf-8')
    for old, new in entry['replace']:
        assert old in text, (entry['path'], old)
        text = text.replace(old, new)
    for old, new in entry.get('optional_replace', []):
        text = text.replace(old, new)
    path.write_bytes(text.encode('utf-8'))
    paths.append(entry['path'])
assert len(paths) == len(set(paths)) == 25
subprocess.run(['git', 'add', '--', *paths], check=True)
subprocess.run(['git', 'diff', '--cached', '--check'], check=True)
subprocess.run(['git', 'diff', '--exit-code'], check=True)
tree = subprocess.check_output(['git', 'write-tree'], text=True).strip()
record = {'base': BASE, 'base_tree': BASE_TREE, 'tree': tree,
          'files': [{'path': p, 'sha': blob((root/p).read_bytes())} for p in paths]}
(root / '.git/punctuation-prepared.json').write_text(json.dumps(record, indent=2) + '\n')
print('PREPARED_RELEASE_TREE=' + tree)
print('Changed exactly 25 authorized files. Main is unchanged.')
