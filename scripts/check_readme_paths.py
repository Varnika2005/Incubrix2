import re

with open('README.md', 'r', encoding='utf-8') as f:
    text = f.read()

paths = re.findall(r'[a-zA-Z]:\\[^\s`"\'\)]+', text)
print("Hardcoded paths found in README.md:", paths)

