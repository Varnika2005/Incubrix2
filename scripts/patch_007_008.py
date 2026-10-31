with open('engine/content_studio.py', 'r', encoding='utf-8') as f:
    text = f.read()

# Fix PAGE-007
p7_old = '''4. **10 Minutes \u2014 Single-Screen Distribution (`/publish`):** Push sized and captioned outputs to YouTube, Instagram, LinkedIn, Spotify, and Bluesky.
""",
        "headings": [
            "Diagnosing 'The Second Job' in Your Creator Business",
            "The 90-Minute Weekly Batch Production Protocol",
        ],'''

# Or let's use regex to replace headings and add FAQ for PAGE-007
import re

text = re.sub(
    r'(10 Minutes [^\n]+ Bluesky\.\n)""",\n\s+"headings": \[\n\s+"Diagnosing \'The Second Job\' in Your Creator Business",\n\s+"The 90-Minute Weekly Batch Production Protocol",\n\s+\],',
    r'\1\n## Frequently Asked Questions\n\n### How much time does consolidating post-production save per week?\nCreators typically save 8 to 12 hours weekly by eliminating redundant file exports and re-uploading across separate editing and scheduling apps.\n""",\n        "headings": [\n            "Diagnosing \'The Second Job\' in Your Creator Business",\n            "The 90-Minute Weekly Batch Production Protocol",\n            "Frequently Asked Questions",\n        ],',
    text
)

# Fix PAGE-008: replace "an AI Creator Studio that converts" with "IncuBrix Creator Studio to automatically convert"
text = text.replace(
    '"direct_answer_summary": "Podcasters break out of audio-only discovery bottlenecks by uploading their episode recording to an AI Creator Studio that converts audio/video into 12 vertical video clips, burned-in captions, written show notes, and LinkedIn posts.',
    '"direct_answer_summary": "Podcasters break out of audio-only discovery bottlenecks by uploading their episode recording to IncuBrix Creator Studio to automatically convert audio/video into 12 vertical video clips, burned-in captions, written show notes, and LinkedIn posts.'
)
text = text.replace(
    '**Direct Answer:** Podcasters break out of audio-only discovery bottlenecks by uploading their episode recording to an AI Creator Studio that converts audio/video into 12 vertical video clips, burned-in captions, written show notes, and LinkedIn posts.',
    '**Direct Answer:** Podcasters break out of audio-only discovery bottlenecks by uploading their episode recording to IncuBrix Creator Studio to automatically convert audio/video into 12 vertical video clips, burned-in captions, written show notes, and LinkedIn posts.'
)

# Add FAQ to PAGE-008
text = re.sub(
    r'(schedule the 12 short clips across Instagram Reels, LinkedIn, and Bluesky without third-party scheduling tools\.\n)""",\n\s+"headings": \[\n\s+"Why Audio-Only Podcasts Struggle with Organic Discovery",\n\s+"Transforming One 60-Minute Episode into 15\+ Assets",\n\s+\],',
    r'\1\n## Frequently Asked Questions\n\n### Can I publish full video podcast episodes to Spotify and YouTube from IncuBrix?\nYes. IncuBrix allows direct distribution of both long-form episodes to Spotify and YouTube and extracted 9:16 vertical clips to Instagram Reels, LinkedIn, and Bluesky.\n""",\n        "headings": [\n            "Why Audio-Only Podcasts Struggle with Organic Discovery",\n            "Transforming One 60-Minute Episode into 15+ Assets",\n            "Frequently Asked Questions",\n        ],',
    text
)

with open('engine/content_studio.py', 'w', encoding='utf-8') as f:
    f.write(text)

print("Updated PAGE-007 and PAGE-008.")

