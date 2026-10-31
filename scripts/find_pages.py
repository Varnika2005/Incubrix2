with open('engine/content_studio.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()
for pid in ['PAGE-007', 'PAGE-008', 'PAGE-009', 'PAGE-010']:
    for i, l in enumerate(lines):
        if f'"page_id": "{pid}"' in l:
            print(f'=== {pid} at line {i} ===')
            print(''.join(lines[i:i+35]))
            break

