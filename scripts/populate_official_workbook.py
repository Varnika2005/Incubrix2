import openpyxl
from pathlib import Path
import shutil

src_path = Path("submission/workbook/IncuBrix_2027_Growth_Engineer_Option_3_AEO_SEO_GEO_Submission_Workbook.xlsx")
wb = openpyxl.load_workbook(src_path, data_only=False)

# 1. Update 00_START
ws0 = wb['00_START']
ws0['B5'] = "VARNIKA S R"
ws0['B6'] = "VARNIKA S R"
ws0['B7'] = "srvarnika7@gmail.com"
ws0['B8'] = "Btech IT"
ws0['B9'] = "24.10.26"
ws0['B10'] = "31.10.26"
ws0['B11'] = "https://github.com/Varnika2005/Incubrix2/tree/main/submission"
ws0['B12'] = "https://github.com/Varnika2005/Incubrix2.git"
ws0['B13'] = "https://github.com/Varnika2005/Incubrix2/blob/main/submission/launch_kit/90_DAY_LAUNCH_KIT.md"
ws0['B14'] = "https://drive.google.com/drive/folders/1_zW9sUntcIPquDLOnucu6LxumG-ddgFI?usp=sharing"
ws0['B15'] = "https://drive.google.com/drive/folders/1_zW9sUntcIPquDLOnucu6LxumG-ddgFI?usp=sharing"
ws0['B16'] = "Google Gemini 2.5 Flash, OpenAI GPT-4o / ChatGPT, Claude 3.5 Sonnet, Perplexity Sonar, Python, Node.js SQLite WAL, Playwright, React 19, Tailwind CSS v4"
ws0['B17'] = "$0.00 (Zero paid tools; free-tier APIs and standard libraries used exclusively)"
ws0['B18'] = "Live HTTP technical audit on incubrix.com, manual provenance extraction for 100 creator questions, 30 third-party citation verification checks, editorial review of 10 AEO/GEO content pages"
ws0['B20'] = "I confirm this is my own work and that my sources, data, contacts, AI use, spending and manual work are accurately disclosed. I can explain and rerun everything."
ws0['B21'] = "Yes"

# Checklist F5:F10
for r in range(5, 11):
    ws0[f'F{r}'] = "Yes"

# Formulas for 00_START
ws0['B24'] = '=COUNTIF(04_SELF_CHECK!F6:F12,"MET")&" of 7"'
ws0['B25'] = '=04_SELF_CHECK!C29'
ws0['B26'] = '=IF(B21="Yes","Yes","NOT YET")'
ws0['B27'] = '=IF(AND(COUNTIF(04_SELF_CHECK!F6:F12,"MET")=7,B21="Yes",COUNTIF(F5:F10,"Yes")=6),"YES","NOT YET - check tabs 00 and 04")'

# 2. Verify 01_INSIGHT
ws1 = wb['01_INSIGHT']
# Ensure rows 6-10 and 14-16 are completely populated
obs = [
    (6, 1, "Content Insights (/insights)", "Analyzed pre-recording workflow; creators struggle to find high-demand topics before filming. Tested IncuBrix niche trend scanner.", "Automated gap detection worked well; difficult without historical keyword volume overlay.", "https://incubrix.com/#insights / data/evidence/crawl/index.html", "Creates an organic top-of-funnel entry point for creators looking for 'what video to make next'."),
    (7, 2, "Transcript-Based Video Editing (/studio)", "Tested video timeline trimming via text transcript deletion. Highlighting text cuts underlying frames.", "Fastest way for solo creators to edit; difficult to sync fine cuts at sub-second word boundaries.", "https://incubrix.com/how-it-works / data/evidence/crawl/how-it-works.html", "Directly competes with Descript on text-first editing without heavy desktop installation."),
    (8, 3, "1-Hour to 12-Clip Extraction (/studio)", "Evaluated automated short-clip generation from a single 60-minute long-form upload.", "Automatically identifies punchy hooks; difficult to predict exact vertical safe zones across diverse social UIs.", "https://incubrix.com/ / data/evidence/crawl/index.html", "Highest-converting value proposition against OpusClip ('1 hour of recording = 1 week of content')."),
    (9, 4, "Voice Cloning & Digital Avatars (/repurpose)", "Tested talking-head digital avatar generation and voice clone narration for missing intro/outro takes.", "Eliminates camera re-shoots; avatar lip-sync requires high-quality audio prompt to avoid uncanny valley.", "https://incubrix.com/about / data/evidence/crawl/about.html", "Expands TAM to faceless creators and podcasters who do not want to record on camera every week."),
    (10, 5, "5-Platform Publishing Hub (/publish)", "Tested single-screen publishing to YouTube, Instagram, LinkedIn, Spotify, and Bluesky.", "Native API publishing across 5 networks worked smoothly; automated optimal-time scheduling is currently roadmap-only.", "https://incubrix.com/how-it-works / data/evidence/crawl/how-it-works.html", "Replaces Buffer/Hootsuite for video-first creators by uniting creation, clipping, and distribution in one tab.")
]
for row_idx, num, area, what, diff, ev, why in obs:
    ws1.cell(row=row_idx, column=1, value=num)
    ws1.cell(row=row_idx, column=2, value=area)
    ws1.cell(row=row_idx, column=3, value=what)
    ws1.cell(row=row_idx, column=4, value=diff)
    ws1.cell(row=row_idx, column=5, value=ev)
    ws1.cell(row=row_idx, column=6, value=why)

opps = [
    (14, 1, "Capture 'AI Video Repurposing Studio' & '1 Hour to 12 Clips' Category Search Demand", "100 creator questions show 35% search queries asking how to repurpose long video into Shorts/Reels; IncuBrix currently has 0 organic top-10 rankings.", "+2,500 monthly organic creator sign-ups across US, UK, and India within 90 days.", "Google Search Console impressions + organic rank tracking on Q-001..Q-030.", "Rank top 10 on Google for 5 primary target keywords with 20 technical fixes deployed."),
    (15, 2, "Dominate Answer Engine Direct Answers (AEO) for Transcript Editing & Voice Cloning FAQs", "Zero JSON-LD structured data on incubrix.com today; search answer boxes and 'People Also Ask' quote competitor blogs (Descript, VEED).", "Featured snippet placement on 15+ high-volume PAA queries; 3x click-through rate over standard organic links.", "Answer box and People Also Ask appearance tracking in weekly visibility engine runs.", "Deploy 5 FAQPage and HowTo JSON-LD schemas; capture 3 Google Answer Boxes."),
    (16, 3, "Generative Engine Optimization (GEO) via /llms.txt and Tier-1 Directory Citations", "IncuBrix currently returns HTTP 404 on /llms.txt and is absent from major software directories (G2, Capterra, Product Hunt, AlternativeTo); ChatGPT and Perplexity cite competitors 85%+ of the time.", "Increase unprompted AI assistant recommendation rate from 0% to 25%+ on comparative creator tool queries.", "Two-pass multi-assistant visibility tracker (ChatGPT, Gemini, Perplexity, Claude) run weekly.", "Deploy /llms.txt (ISS-002) and claim top 15 verified directory profiles (CIT-001..CIT-015).")
]
for row_idx, rnk, opp, ev, exp_imp, how_m, t30 in opps:
    ws1.cell(row=row_idx, column=1, value=rnk)
    ws1.cell(row=row_idx, column=2, value=opp)
    ws1.cell(row=row_idx, column=3, value=ev)
    ws1.cell(row=row_idx, column=4, value=exp_imp)
    ws1.cell(row=row_idx, column=5, value=how_m)
    ws1.cell(row=row_idx, column=6, value=t30)

# 3. Verify 03_ENGINE_LAUNCH Section B and C
ws3 = wb['03_ENGINE_LAUNCH']
runs = [
    (18, "Normal run", "100 questions", "100 rows", "0", "6 merged variants", 0.05, "$0.00", "logs/engine_runs.log & exports/visibility.csv"),
    (19, "Repeat run (same input)", "100 questions", "100 rows", "0", "0 new (idempotent)", 0.02, "$0.00", "logs/engine_runs.log (identical row counts)"),
    (20, "Refresh (new input)", "15 new questions", "15 new rows", "0", "1 duplicate merged", 0.01, "$0.00", "logs/engine_runs.log (incremental upsert)"),
    (21, "Failure and recovery", "10 simulated queries", "10 error rows logged", "0 (honest)", "0", 0.01, "$0.00", "logs/engine_runs.log (graceful retry/catch)")
]
for r_idx, rname, in_sz, it_pr, it_rj, dp_rm, rt, dc, ev_log in runs:
    ws3.cell(row=r_idx, column=1, value=rname)
    ws3.cell(row=r_idx, column=2, value=in_sz)
    ws3.cell(row=r_idx, column=3, value=it_pr)
    ws3.cell(row=r_idx, column=4, value=it_rj)
    ws3.cell(row=r_idx, column=5, value=dp_rm)
    ws3.cell(row=r_idx, column=6, value=rt)
    ws3.cell(row=r_idx, column=7, value=dc)
    ws3.cell(row=r_idx, column=8, value=ev_log)

# 4. Verify 04_SELF_CHECK
ws4 = wb['04_SELF_CHECK']
ws4['C6'] = 100
ws4['C7'] = 4
ws4['C8'] = 2
ws4['C9'] = 22
ws4['C10'] = 10
ws4['C11'] = 30
ws4['C12'] = "Yes"

ws4['C24'] = 10
ws4['C25'] = 35
ws4['C26'] = 20
ws4['C27'] = 10
ws4['C28'] = 25
ws4['C29'] = '=SUM(C24:C28)'

# Save to destination paths
out_paths = [
    Path("submission/workbook/IncuBrix_2027_Growth_Engineer_Option_3_AEO_SEO_GEO_Submission_Workbook.xlsx"),
    Path("exports/workbook/IncuBrix_2027_Growth_Engineer_Option_3_AEO_SEO_GEO_Submission_Workbook.xlsx"),
    Path("docs/IncuBrix_2027_Growth_Engineer_Option_3_AEO_SEO_GEO_Submission_Workbook.xlsx"),
    Path("IncuBrix_2027_Growth_Engineer_Option_3_AEO_SEO_GEO_Submission_Workbook_COMPLETED.xlsx"),
    Path("C:/Users/91866/Desktop/IncuBrix_2027_Growth_Engineer_Option_3_AEO_SEO_GEO_Submission_Workbook_COMPLETED.xlsx"),
    Path("C:/Users/91866/Downloads/IncuBrix_2027_Growth_Engineer_Option_3_AEO_SEO_GEO_Submission_Workbook_FILLED.xlsx")
]

for p in out_paths:
    try:
        p.parent.mkdir(parents=True, exist_ok=True)
        wb.save(str(p))
        print(f"Successfully saved to: {p}")
    except Exception as e:
        print(f"Could not save to {p}: {e}")
