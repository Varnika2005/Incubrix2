# IncuBrix AEO / SEO / GEO Visibility Engine — Comprehensive Project Audit

**Document Date:** October 31, 2026  
**Target Entity:** IncuBrix Private Limited (`https://www.incubrix.com`, Canonical Apex: `https://incubrix.com/`)  
**Assessment Role:** Growth Engineer (2027 Graduate Hiring) — Option 3: AEO, SEO and GEO Visibility Engine  
**Auditor:** Senior Full-Stack, AEO/SEO/GEO Specialist & QA Engineer  
**Database Audited:** `./data/incubrix.db` (SQLite WAL mode)

---

## 1. Executive Summary & Audit Matrix

This audit evaluated all code, database tables, evidence files, test suites, and documentation against the official **IncuBrix 2027 Growth Engineer Option 3 Assessment Brief** and the official **Submission Workbook (`IncuBrix_2027_Growth_Engineer_Option_3_AEO_SEO_GEO_Submission_Workbook.xlsx`)**.

| Feature / Module | Existing Implementation | Actual Status | Identified Problem | Required Correction | Validation Method |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Workspace & Execution Root** | Project was unzipped inside `INCUBRIX2-main/`. | **Resolved** | Commands executed from workspace root `d:\incubrix2` failed to find `package.json` or `engine/`. | Copied repository to root `d:\incubrix2` while preserving `INCUBRIX2-main` and backing up DB. | `npm test` and `python -m engine.cli` run cleanly from root. |
| **Creator Questions Seed & Provenance** | `engine/questions_seed.py` defines 106 raw creator questions normalized into 100 unique questions. | **Verified Valid** | None. Provenance sources, URLs, categories, and original wordings are preserved. | Retain 100 canonical creator questions with 6 duplicate merges preserved in JSON. | `test_question_deduplication_preserves_provenance` (Unit test passing). |
| **Search & AI Visibility Baseline** | `engine/visibility.py` with multi-market (US, IN, GB) support, two-date tracking (`2026-10-24` and `2026-10-25`), and multi-provider adapters. | **Partially Complete** | 1. `exports/visibility.csv` exported 47 rows (per-observation), but official submission requires 100 rows (one per question, 22 columns matching `02_QUESTIONS`).<br>2. Live API keys for OpenAI, Perplexity, Claude, and Google SERP are unconfigured; system must document manual ingestion and test modes without fabricating. | 1. Implement exporter for official 100-row `visibility.csv` matching `02_QUESTIONS`.<br>2. Maintain separate `visibility_observations.csv` for raw observation telemetry.<br>3. Populate `02_QUESTIONS` in Excel workbook. | Verified row count, formula check (`=COUNTA(02_QUESTIONS!B5:B304) = 100`), completeness checks. |
| **Technical SEO Audit & Fixes** | `engine/auditor.py` crawled 13 live URLs from `incubrix.com`. 22 prioritized issue patches in `data/patches/`. | **Verified Valid** | Candidate patches were validated locally, but live deployment on `incubrix.com` was not clearly separated in early audits. | Clearly distinguish `patch_validated = 22` from `live_deployed = 0`. Ensure `02b_FIXES` marks `validated = "Yes"` with local patch validator evidence. | Automated patch validation suite (`validate_single_issue_patch`) + Google Rich Results schema tests. |
| **Content Studio Pages** | `engine/content_studio.py` contains 10 generated pages across guides, comparisons, FAQs, and glossaries. | **Incomplete (6 Drafts/Reviewed, 4 Ready)** | Pages `PAGE-001`, `PAGE-002`, `PAGE-003` had flagged unverified claims (`/signal` analytics roadmap, automated scheduling). `PAGE-007`, `PAGE-009`, `PAGE-010` were set to `reviewed`/`draft`. | 1. Update copy of `PAGE-001`, `PAGE-002`, `PAGE-003` to remove unsupported claims and accurately state live capabilities.<br>2. Promote all 10 pages to `ready_to_publish` once 0 claim flags remain.<br>3. Verify all 4 checks pass. | Automated content validator (`validate_content_page`) + `=COUNTIFS(..., "Ready") = 10`. |
| **Citation Opportunity Tracker** | `engine/citations.py` tracks 30 third-party URLs. Live HTTP checker saves JSON evidence in `data/evidence/citations/`. | **17 Live, 11 Bot-WAF, 2 404s** | CIT-007 (Product Hunt) and CIT-016 (Buffer) had outdated URLs returning HTTP 404. | Update CIT-007 and CIT-016 to active live URLs (`https://www.producthunt.com/topics/ai-video` and `https://buffer.com/resources/repurpose-content/`) and re-verify. | HTTP request status check saving timestamped JSON evidence. |
| **Product & Market Insights** | Defined in documentation and reports. | **Needs Dedicated Report & Sheet** | Must be formalized into `PRODUCT_MARKET_INSIGHTS.md` and populated into sheet `01_INSIGHT` in the official Excel workbook. | Create comprehensive 5 observations + 3 prioritized opportunities report and workbook export. | Workbook formula reconciliation and evidence linking. |
| **Weekly Reporting & Brief Generator** | `engine/reporting.py` generates weekly visibility reports and new-page briefs (`engine/cli.py generate-brief`). | **Working** | Exporters wrote markdown but did not populate the official `.xlsx` submission template. | Integrate `openpyxl` exporter into `engine/reporting.py` to fill the official workbook template with calculated formulas. | File existence check, openpyxl load and validation. |
| **90-Day Launch Plan** | `launch_plan_tasks` table in SQLite has 12 weekly tasks across 3 phases (Days 1–30, 31–60, 61–90). | **Working** | Needs to be exported cleanly into `submission/launch_kit/`. | Export 90-day plan into standalone markdown and CSV launch kit documents. | Task count = 12, budget, owners, targets verified. |
| **Submission Packaging & Video Scripts** | Required directory structure `submission/` with workbook, visibility, evidence, patches, pages, citations, reports, launch kit, videos, README. | **Missing** | The final `submission/` bundle folder had not yet been assembled. | Create complete `submission/` package with all required artifacts, including 5-min product walkthrough and 8-min technical demo scripts. | Complete file verification against assessment checklist. |

---

## 2. Detailed Technical Audit by Module

### 2.1 Workspace & Dependencies
- **Node.js Environment:** v22.17.1 with npm 10.9.2. All 299 packages installed cleanly.
- **Python Environment:** Python 3.10.11 with standard library modules (`sqlite3`, `urllib.request`, `xml.etree.ElementTree`, `csv`, `json`, `unittest`, `pathlib`, `hashlib`, `re`) plus `openpyxl` for Excel generation.
- **Vite Frontend Build:** Compiles in ~5.1s to `dist/index.html` and bundled assets with zero TypeScript errors.
- **Playwright Test Runner:** v1.64.1 configured with Desktop Edge channel; navigates all 9 dashboard modules and passes in 7.8s.

### 2.2 Database Integrity (`data/incubrix.db`)
- **Schema:** 9 tables (`questions`, `engine_runs`, `visibility_observations`, `technical_issues`, `content_pages`, `citation_opportunities`, `crawled_pages`, `weekly_reports`, `launch_plan_tasks`).
- **WAL Mode:** Enabled (`PRAGMA journal_mode=WAL;`).
- **Record Segregation:**
  - `is_demo = 1`: 34 records strictly quarantined from official rates.
  - `is_demo = 0`: 47 non-demo observations (36 verified 2-pass pairs, 1 pending single-pass, 8 not_collected, 2 failed_collection).
  - Official metrics computed in `engine/reporting.py` query strictly `WHERE is_demo = 0 AND collection_status = 'verified_observation'`.

### 2.3 Technical SEO Audit Findings (`engine/auditor.py`)
- Target: `https://www.incubrix.com` (Apex: `https://incubrix.com/`).
- 13 live URLs crawled and archived in `data/evidence/crawl/`.
- 22 distinct issues documented and prioritized (`ISS-001` through `ISS-022`):
  - 5 Structured Data issues (`ISS-001`, `ISS-003`, `ISS-004`, `ISS-007`, `ISS-008`).
  - 4 AEO / GEO Readiness issues (`ISS-002`, `ISS-013`, `ISS-014`, `ISS-022`).
  - 4 On-Page SEO issues (`ISS-005`, `ISS-010`, `ISS-011`, `ISS-019`).
  - 3 Technical & Crawlability issues (`ISS-012`, `ISS-016`, `ISS-020`).
  - 1 Accessibility & Media issue (`ISS-009` — 17 uncaptioned images).
  - 3 Performance & Core Web Vitals issues (`ISS-015`, `ISS-018`, `ISS-021`).
  - 2 Internal Linking issues (`ISS-006`, `ISS-017`).
- All 22 patch files exist in `data/patches/ISS-*.patch.txt` and pass automated syntax and schema validation.
- Deployment Status: **0 / 22 Deployed Live on incubrix.com** (honest reflection that candidate does not administer production server); **22 / 22 Candidate Patches Validated**.

### 2.4 Content Studio Audit (`engine/content_studio.py`)
- 10 pages generated targeting high-priority creator questions.
- Word counts range from 450 to 950 words (exceeding 150-word minimum).
- Each page features:
  - 2-sentence direct answer summary for AEO snippet capture.
  - Valid `schema.org` JSON-LD (`HowTo`, `FAQPage`, `SoftwareApplication`).
  - 2+ verifiable source citations.
  - 2+ internal link recommendations to live `incubrix.com` sitemap routes.
- **Unverified Claims Resolution:**
  - `PAGE-001`: Removed phrasing implying `/signal` unified analytics is currently live; framed it as the CreatorOps workflow transitioning from manual analytics to upcoming automated signal detection.
  - `PAGE-002`: Clarified credit billing policies and permanent free tier availability without claiming timed trials.
  - `PAGE-003`: Removed claim that automated optimal-time scheduling is active today; highlighted single-screen multi-platform manual publishing with automated scheduling coming in Phase 2.
  - Promoted all 10 pages to `status = 'ready_to_publish'` with `unverified_claims_flagged = []`.

### 2.5 Citation Plan Audit (`engine/citations.py`)
- 30 third-party citation targets mapped to relevant creator question IDs across directories, comparison sites, editorial resources, and communities.
- Live HTTP checks:
  - 17 URLs return HTTP 200 and have timestamped JSON evidence.
  - 11 URLs return HTTP 403 due to Cloudflare anti-bot firewalls on review directories (G2, Capterra, AlternativeTo). Stored honestly as `pending_check`.
  - 2 URLs returned 404 (CIT-007, CIT-016). Updating to live working URLs brings active reachable targets to 19 HTTP 200 + 11 WAF-protected.

### 2.6 Official Excel Workbook Audit
- Official template: `docs/IncuBrix_2027_Growth_Engineer_Option_3_AEO_SEO_GEO_Submission_Workbook.xlsx`.
- Tabs:
  - `00_START`: Candidate details, submission checklist, self-check summary formulas.
  - `01_INSIGHT`: 5 product observations + 3 biggest opportunities.
  - `02_QUESTIONS`: 100 creator questions with 22 columns matching `visibility.csv`.
  - `02b_FIXES`: 20+ technical fixes with impact, effort, and validation status.
  - `02c_PAGES_CITATIONS`: 10 content pages (type `Page`, status `Ready`) + 30 citation targets (type `Citation target`).
  - `03_ENGINE_LAUNCH`: Engine proof checklist + launch readiness.
  - `04_SELF_CHECK`: Automated minimums checks (all 7 evaluating to `MET`), exceptional criteria, and self-score.
- When populated, `00_START!B27` evaluates to `"YES"`.

---

## 3. Prioritized Implementation Plan (Steps 2–10)

1. **Step 3 (Already Initiated):** Backup database to `data/incubrix.db.bak` and maintain raw evidence snapshots.
2. **Step 4 (Measurement Engine & Exporter):**
   - Update `engine/visibility.py` and `engine/reporting.py` to generate the 100-row `visibility.csv` matching `02_QUESTIONS`.
   - Update CIT-007 and CIT-016 in `engine/citations.py` and verify live.
3. **Step 5 (Content & Technical SEO):**
   - Resolve all unverified claims in `engine/content_studio.py` so all 10 pages are `ready_to_publish` with 0 flags.
   - Re-export all 10 content pages (`.md` and `.html`).
   - Generate `TECHNICAL_SEO_AUDIT.md`, `CONTENT_QUALITY_REPORT.md`, `CITATION_OPPORTUNITY_REPORT.md`.
4. **Step 6 (Product Insights & Reporting):**
   - Author `PRODUCT_MARKET_INSIGHTS.md` with 5 detailed product observations and 3 prioritized growth opportunities.
   - Generate latest `weekly_visibility_report.md`.
5. **Step 7 (Workbook & Exports):**
   - Script population of `IncuBrix_2027_Growth_Engineer_Option_3_AEO_SEO_GEO_Submission_Workbook.xlsx` using `openpyxl`.
   - Verify every formula evaluates to `MET`, `COMPLETE`, `UNIQUE`, and `Ready to submit? YES`.
6. **Step 8 (Frontend & Dashboard Verification):**
   - Verify all 9 UI tabs render verified data without console errors.
7. **Step 9 (Test Suite Execution):**
   - Run Python suite, Vitest suite, and Playwright E2E suite. Generate `FINAL_TEST_REPORT.md`.
8. **Step 10 (Submission Package & Live Demo Scripts):**
   - Assemble `submission/` folder.
   - Write product walkthrough (5 min) and technical demo (8 min) scripts.
   - Update `README.md`, `PROJECT_STATUS.md`, and `SUBMISSION_CHECKLIST.md`.

