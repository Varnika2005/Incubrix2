import re

with open('engine/content_studio.py', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Fix PAGE-004 title
content = content.replace(
    '"title": "How to Create Talking-Head Videos & Podcast Narration with AI Voice Cloning and Digital Avatars",',
    '"title": "How to Create Talking-Head Videos with AI Voice Cloning & Avatars",'
)

# 2. Add FAQ to PAGE-004
page_004_target = '''### 4. Consent, Privacy, and Governance Best Practices
Always use only your own voice and likeness (or explicitly authorized team members\' likenesses) in accordance with **IncuBrix Terms of Service** (`https://incubrix.com/terms`) and **Privacy Policy** (`https://incubrix.com/privacy`).
""",
        "headings": [
            "When to Use Digital Avatars and Voice Cloning in a Creator Workflow",
            "Step-by-Step Workflow in IncuBrix Creator Studio",
        ],'''

page_004_replacement = '''### 4. Consent, Privacy, and Governance Best Practices
Always use only your own voice and likeness (or explicitly authorized team members\' likenesses) in accordance with **IncuBrix Terms of Service** (`https://incubrix.com/terms`) and **Privacy Policy** (`https://incubrix.com/privacy`).

## Frequently Asked Questions

### Can I use AI voice cloning for commercial YouTube and Spotify content?
Yes. IncuBrix provides commercial usage rights for trained personal voice models under the Starter ($10/mo) through Pro ($250/mo) plans.
""",
        "headings": [
            "When to Use Digital Avatars and Voice Cloning in a Creator Workflow",
            "Step-by-Step Workflow in IncuBrix Creator Studio",
            "Frequently Asked Questions",
        ],'''

content = content.replace(page_004_target, page_004_replacement)

# 3. Add FAQ to PAGE-007
page_007_target = '''### 3. Reinvesting Saved Hours into Keystone Content
By automating the tedious mechanics of clipping, subtitle alignment, and multi-network uploads, creators redirect their energy toward high-leverage creative tasks: interviewing better guests, sharpening video hooks, and engaging with their core community.
""",
        "headings": [
            "Diagnosing 'The Second Job' in Your Creator Business",
            "The Unified CreatorOps Consolidation Workflow",
        ],'''

page_007_replacement = '''### 3. Reinvesting Saved Hours into Keystone Content
By automating the tedious mechanics of clipping, subtitle alignment, and multi-network uploads, creators redirect their energy toward high-leverage creative tasks: interviewing better guests, sharpening video hooks, and engaging with their core community.

## Frequently Asked Questions

### How much time does consolidating post-production save per week?
Creators typically save 8 to 12 hours weekly by eliminating redundant file exports and re-uploading across separate editing and scheduling apps.
""",
        "headings": [
            "Diagnosing 'The Second Job' in Your Creator Business",
            "The Unified CreatorOps Consolidation Workflow",
            "Frequently Asked Questions",
        ],'''

content = content.replace(page_007_target, page_007_replacement)

# 4. Fix PAGE-008 direct answer and add FAQ
page_008_target = '''"direct_answer_summary": "Podcasters break out of audio-only discovery bottlenecks by uploading their episode recording to an AI Creator Studio that converts audio/video into 12 vertical video clips, burned-in captions, written show notes, and LinkedIn posts. From the same screen, hosts can distribute the full episode to Spotify and YouTube while fanning out short teaser clips to Instagram, LinkedIn, and Bluesky.",
        "body_markdown": """# Podcast-to-Video Repurposing Guide: Grow Your Show on YouTube, Spotify, Reels & LinkedIn

**Direct Answer:** Podcasters break out of audio-only discovery bottlenecks by uploading their episode recording to an AI Creator Studio that converts audio/video into 12 vertical video clips, burned-in captions, written show notes, and LinkedIn posts. From the same screen, hosts can distribute the full episode to Spotify and YouTube while fanning out short teaser clips to Instagram, LinkedIn, and Bluesky.

---

## The Discoverability Problem of Audio-Only Podcasting'''

page_008_replacement = '''"direct_answer_summary": "Podcasters break out of audio-only discovery bottlenecks by uploading their episode recording to IncuBrix Creator Studio to automatically convert audio/video into 12 vertical video clips, burned-in captions, written show notes, and LinkedIn posts. From the same screen, hosts can distribute the full episode to Spotify and YouTube while fanning out short teaser clips to Instagram, LinkedIn, and Bluesky.",
        "body_markdown": """# Podcast-to-Video Repurposing Guide: Grow Your Show on YouTube, Spotify, Reels & LinkedIn

**Direct Answer:** Podcasters break out of audio-only discovery bottlenecks by uploading their episode recording to IncuBrix Creator Studio to automatically convert audio/video into 12 vertical video clips, burned-in captions, written show notes, and LinkedIn posts. From the same screen, hosts can distribute the full episode to Spotify and YouTube while fanning out short teaser clips to Instagram, LinkedIn, and Bluesky.

---

## The Discoverability Problem of Audio-Only Podcasting'''

content = content.replace(page_008_target, page_008_replacement)

page_008_headings_target = '''### 4. Single-Screen Distribution
Push the full episode to Spotify and YouTube with automated metadata, and schedule the 12 short clips across Instagram Reels, LinkedIn, and Bluesky without third-party scheduling tools.
""",
        "headings": [
            "The Discoverability Problem of Audio-Only Podcasting",
            "The 4-Step Podcast-to-Video Repurposing Flywheel",
        ],'''

page_008_headings_replacement = '''### 4. Single-Screen Distribution
Push the full episode to Spotify and YouTube with automated metadata, and schedule the 12 short clips across Instagram Reels, LinkedIn, and Bluesky without third-party scheduling tools.

## Frequently Asked Questions

### Can I publish full video podcast episodes to Spotify and YouTube from IncuBrix?
Yes. IncuBrix allows direct distribution of both long-form episodes to Spotify and YouTube and extracted 9:16 vertical clips to Instagram Reels, LinkedIn, and Bluesky.
""",
        "headings": [
            "The Discoverability Problem of Audio-Only Podcasting",
            "The 4-Step Podcast-to-Video Repurposing Flywheel",
            "Frequently Asked Questions",
        ],'''

content = content.replace(page_008_headings_target, page_008_headings_replacement)

# 5. Add FAQ to PAGE-009
page_009_target = '''## Why Hybrid Creators Need Both Real Footage & Digital Avatars

Most authentic creators film real long-form episodes when they have time, and rely on **voice cloning + digital avatars** to fill in short scripts, intros, or daily commentary when they are away from the studio. IncuBrix is purpose-built for this hybrid workflow.
""",
        "headings": [
            "Point Solutions vs Unified Creator Studio",
            "Why Hybrid Creators Need Both Real Footage & Digital Avatars",
        ],'''

page_009_replacement = '''## Why Hybrid Creators Need Both Real Footage & Digital Avatars

Most authentic creators film real long-form episodes when they have time, and rely on **voice cloning + digital avatars** to fill in short scripts, intros, or daily commentary when they are away from the studio. IncuBrix is purpose-built for this hybrid workflow.

## Frequently Asked Questions

### How does IncuBrix compare to HeyGen and ElevenLabs?
While HeyGen focuses primarily on digital avatars and ElevenLabs on voice generation, IncuBrix unifies transcript video editing, 12-clip highlight extraction, voice cloning, avatars, and 5-platform social publishing in one platform.
""",
        "headings": [
            "Point Solutions vs Unified Creator Studio",
            "Why Hybrid Creators Need Both Real Footage & Digital Avatars",
            "Frequently Asked Questions",
        ],'''

content = content.replace(page_009_target, page_009_replacement)

# 6. Fix PAGE-010 headings
page_010_target = '''        "headings": [
            "Frequently Asked Creator Questions",
        ],'''

page_010_replacement = '''        "headings": [
            "Frequently Asked Creator Questions",
            "Safe-Zone Caption Placement & Retention Rules",
            "Publishing & AEO Optimization Best Practices",
        ],'''

content = content.replace(page_010_target, page_010_replacement)

with open('engine/content_studio.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("Updated engine/content_studio.py successfully.")

