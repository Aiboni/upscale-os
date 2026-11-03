"""Create labels and GitHub issues from _docs/issues-groomed.md using the GitHub CLI (gh).
Usage:  py tools/create_issues.py --dry-run     (only print)
        py tools/create_issues.py               (create mvp + post-mvp issues)
        py tools/create_issues.py --bugs        (also create user-test-bug drafts - confirm them first!)
Issues are created OPEN. Close them only after a real QA PASS comment."""
import re
import subprocess
import sys
from pathlib import Path

dry = '--dry-run' in sys.argv
with_bugs = '--bugs' in sys.argv
text = Path('_docs/issues-groomed.md').read_text(encoding='utf-8')
pat = re.compile(r"### (?:Bug )?\d+\. (.+?)\n\*\*Label:\*\* `(.+?)`.*?```markdown\n(.*?)```", re.S)
items = [(t.strip(), l, b.strip()) for t, l, b in pat.findall(text)]
if not with_bugs:
    items = [i for i in items if i[1] != 'user-test-bug']

def run(cmd):
    print(' '.join(cmd[:4]) + ' ...')
    if not dry:
        subprocess.run(cmd, check=True)

for name, color in [('mvp', '7553ef'), ('post-mvp', '9393a4'), ('user-test-bug', 'd73a4a')]:
    run(['gh', 'label', 'create', name, '--color', color, '--force'])
for title, label, body in items:
    run(['gh', 'issue', 'create', '--title', title, '--body', body, '--label', label])
print(f'{len(items)} issues', 'planned' if dry else 'created')
