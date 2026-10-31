with open('engine/content_studio.py', 'r', encoding='utf-8') as f:
    text = f.read()

import re
m = re.search(r'"page_id": "PAGE-008".*?"body_markdown": """(.*?)"""', text, re.S)
if m:
    body = m.group(1)
    print("PAGE-008 body end:")
    print(body[-500:])
    print("Does body contain '?':", "?" in body)
    print("Does body contain 'FAQ':", "FAQ" in body)

