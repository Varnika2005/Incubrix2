# IncuBrix 2027 Growth Engineer Assessment — Option 3 Submission

**Candidate:** Growth Engineer Candidate  
**Assessment:** IncuBrix Private Limited 2027 Graduate Hiring — Option 3: AEO, SEO & GEO Visibility Engine  
**Target Property:** `https://www.incubrix.com` (Canonical Apex: `https://incubrix.com/`)  
**Submission Date:** October 31, 2026  

---

## 1. Submission Package Contents

This folder contains all required deliverables specified in Section 4 of the official IncuBrix assessment brief:

```
submission/
├── workbook/
│   ├── IncuBrix_2027_Growth_Engineer_Option_3_AEO_SEO_GEO_Submission_Workbook.xlsx  # Official filled Excel template
│   ├── 01_creator_questions_100.csv                                                # 100 questions with provenance
│   ├── 02_visibility_observations.csv                                              # Multi-market observation telemetry
│   ├── 03_technical_seo_fixes_22.csv                                               # 22 prioritized technical fixes
│   ├── 04_content_studio_10_pages.csv                                              # 10 publish-ready AEO/GEO pages
│   ├── 05_citation_opportunities_30.csv                                            # 30 verified third-party targets
│   ├── 06_launch_plan_90_days.csv                                                  # 12-week implementation tasks
│   └── assessment_workbook_bundle.json                                             # Machine-readable completeness audit
├── visibility/
│   ├── visibility.csv                                                              # Official 100-row file (matches 02_QUESTIONS)
│   └── visibility_observations.csv                                                 # Raw per-pass observation telemetry
├── evidence/
│   ├── crawl/                                                                      # 13 raw HTML crawl snapshots of incubrix.com
│   ├── observations/                                                               # 76 raw JSON AI/Search response evidence files
│   ├── citations/                                                                  # 30 HTTP verification JSON evidence files
│   └── live_gemini_verified.json                                                   # Raw 2-pass Gemini observation payloads
├── technical_fixes/
│   ├── TECHNICAL_SEO_AUDIT.md                                                      # Detailed 22-issue technical audit report
│   └── patches/                                                                    # 22 ready-to-paste patch text files (ISS-001..022)
├── content_pages/
│   ├── CONTENT_QUALITY_REPORT.md                                                   # Page-by-page editorial & schema audit
│   ├── *.md                                                                        # 10 publish-ready Markdown pages
│   └── *.html                                                                      # 10 semantic HTML pages with JSON-LD
├── citation_plan/
│   ├── CITATION_OPPORTUNITY_REPORT.md                                              # 30 detailed citation profiles & earning angles
│   └── citation_opportunities_30.csv                                               # Structured CSV export
├── reports/
│   ├── PROJECT_AUDIT.md                                                            # End-to-end repository & data audit
│   ├── PROJECT_STATUS.md                                                           # Current verified deliverable counts & states
│   ├── PRODUCT_MARKET_INSIGHTS.md                                                  # 5 product observations + 3 growth opportunities
│   ├── FINAL_TEST_REPORT.md                                                        # Full test execution report (14/14 tests pass)
│   ├── SUBMISSION_CHECKLIST.md                                                     # Complete deliverable verification checklist
│   └── weekly_visibility_report.md                                                 # Weekly visibility & variance report
├── launch_kit/
│   ├── 90_DAY_LAUNCH_KIT.md                                                        # 90-day execution plan (Weeks 1–12)
│   └── 06_launch_plan_90_days.csv                                                  # Structured task CSV
└── videos/
    ├── PRODUCT_WALKTHROUGH_SCRIPT.md                                               # 5-minute unedited walkthrough script
    ├── TECHNICAL_DEMO_SCRIPT.md                                                    # 8-minute technical demo script
    └── VIDEO_RECORDING_GUIDE.md                                                    # Video recording & URL linking guide
```

---

## 2. Quick-Start Evaluation Instructions

### A. Run Application & Dashboard
```powershell
# 1. Install dependencies & initialize database
npm run setup

# 2. Launch Express API (http://localhost:3001) & React Frontend (http://localhost:5173)
npm start
```

### B. Run Automated Verification Tests
```powershell
# Run the complete test suite (Python + Vitest + Playwright)
npm run test:all
```

### C. Verify Workbook Calculations
Open `submission/workbook/IncuBrix_2027_Growth_Engineer_Option_3_AEO_SEO_GEO_Submission_Workbook.xlsx`:
- **`00_START`**: Cell **`B24`** displays `"7 of 7"`; cell **`B27`** displays **`"YES"`**.
- **`04_SELF_CHECK`**: All 7 minimum criteria in column **`F`** evaluate to **`"MET"`**.
- **`02_QUESTIONS`**: Exactly 100 rows matching `visibility/visibility.csv`.
- **`02b_FIXES`**: 22 validated technical fixes (`validated = Yes`).
- **`02c_PAGES_CITATIONS`**: 10 Pages (`status = Ready`) and 30 Citation targets.

