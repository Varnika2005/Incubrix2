with open('engine/content_studio.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, l in enumerate(lines):
    if 'for email subscribers.' in l and lines[i+1].strip() == '""",':
        lines.insert(i+1, '\n## Frequently Asked Questions\n\n### Can I publish full video podcast episodes to Spotify and YouTube from IncuBrix?\nYes. IncuBrix allows direct distribution of both long-form episodes to Spotify and YouTube and extracted 9:16 vertical clips to Instagram Reels, LinkedIn, and Bluesky.\n')
        for j in range(i+2, i+25):
            if '"Transforming One 60-Minute Episode into 15+ Assets",' in lines[j]:
                lines.insert(j+1, '            "Frequently Asked Questions",\n')
                break
        print("Inserted FAQ into PAGE-008!")
        break

with open('engine/content_studio.py', 'w', encoding='utf-8') as f:
    f.writelines(lines)
