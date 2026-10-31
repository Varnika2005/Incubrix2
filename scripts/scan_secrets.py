import os
import re

PATTERNS = [
    re.compile(r'sk-[a-zA-Z0-9_-]{20,}'),
    re.compile(r'AQ\.Ab8[a-zA-Z0-9_-]{20,}'),
    re.compile(r'AIzaSy[a-zA-Z0-9_-]{30,}'),
]

IGNORE_DIRS = {'.git', 'node_modules', 'dist', '__pycache__', '.pytest_cache'}
IGNORE_FILES = {'.env'} # .env is in .gitignore

found_secrets = []

for root, dirs, files in os.walk('.'):
    dirs[:] = [d for d in dirs if d not in IGNORE_DIRS]
    for file in files:
        if file in IGNORE_FILES:
            continue
        filepath = os.path.join(root, file)
        try:
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                for pat in PATTERNS:
                    matches = pat.findall(content)
                    if matches:
                        found_secrets.append((filepath, matches))
        except Exception:
            pass

print(f"Secret scan completed. Found secrets: {len(found_secrets)}")
for fp, m in found_secrets:
    print(f"  {fp}: {len(m)} occurrences")

