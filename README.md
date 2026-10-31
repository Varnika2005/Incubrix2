# IncuBrix AEO / SEO / GEO Visibility Engine

**Growth Engineer Assessment — Option 3: AEO, SEO and GEO Visibility Engine**  
**Target Property:** `https://www.incubrix.com` (Canonical Apex: `https://incubrix.com/`)

A full-stack, evidence-backed Search Engine Optimization (SEO), Answer Engine Optimization (AEO), and Generative Engine Optimization (GEO) intelligence platform and CLI engine built to make **IncuBrix Creator Studio** discoverable when creators search for AI tools to ideate, edit via transcript, extract clips, clone voices, generate digital avatars, repurpose across 10+ formats, and publish across YouTube, Instagram, LinkedIn, Spotify, and Bluesky.

---

## Single-Command Quick Start (Windows PowerShell)

```powershell
# 1. Install dependencies, initialize SQLite database, run live HTTP audit on incubrix.com,
#    validate 22 technical patches, seed 100 creator questions, 10 content pages,
#    30 citation targets, 90-day launch plan, and generate all CSV/Workbook exports:
npm run setup

# 2. Launch the Backend API (http://localhost:3001) + Light-Theme Dashboard (http://localhost:5173):
npm start
```

*(If `npm install` has already been run, `npm start` initializes the database and starts both the Express API server and the Vite React frontend concurrently.)*

---

## Hosting Online (Cloud Deployment)

The project includes a production build pipeline where Express serves both the **backend API** and the **built React frontend (`dist/`)** on a single port (`PORT`).

### Option 1: Render.com (Recommended Free/Low-Cost Cloud)
1. Push this repository to GitHub or GitLab.
2. Sign in to [Render.com](https://render.com) and click **New +** $\rightarrow$ **Web Service**.
3. Select **Docker** environment (or let Render detect `render.yaml` automatically).
4. Set Environment Variables (optional: add any available `OPENAI_API_KEY`, `SERPAPI_API_KEY`, etc.).
5. (Recommended) Under **Disks**, add a 1GB persistent disk mounted to `/app/data` to persist your SQLite database across restarts.
6. Click **Deploy**. Your app will be live at `https://your-app-name.onrender.com`.

### Option 2: Railway.app
1. Create a new project on [Railway.app](https://railway.app) $\rightarrow$ **Deploy from GitHub repo**.
2. Railway detects the `Dockerfile` automatically.
3. Add a Persistent Volume mounted at `/app/data`.
4. Expose `PORT=3001` or let Railway assign its `$PORT`.

### Option 3: Docker & Docker Compose (Any VPS / DigitalOcean / Hetzner / AWS)
```bash
# Build and run container in detached mode
docker compose up -d --build

# View container logs
docker compose logs -f
```
The application will be live at `http://your-server-ip:3001`.

---

## Architecture & Tech Stack

- **Frontend (`src/`):** React 19 + Vite + TypeScript + Tailwind CSS v4 + Recharts + Lucide Icons (Light-theme editorial analytics UI with responsive container-query sticky tables).
- **Backend API (`server/`):** Node.js + Express + TypeScript + **Zod** request validation + `node:sqlite` sharing `./data/incubrix.db`.
- **Research, Crawl & Automation Engine (`engine/`):** Python 3 (`sqlite3`, `urllib.request`, `xml.etree.ElementTree`, `csv`, `json`, `unittest`) providing zero-dependency cross-platform execution for live website auditing, JSON-LD validation, question deduplication, multi-market visibility tracking, content brief generation, and workbook exports.
- **Database (`data/incubrix.db`):** Local reproducible SQLite database in WAL mode with raw HTML/JSON evidence stored in `data/evidence/` and code patches in `data/patches/`.
- **Automated Testing (`tests/`):**
  - Python Engine Unit/Integration Tests (`tests/python/test_engine_suite.py` — 7 tests)
  - Backend API & Zod Validation Tests (`tests/unit/api.test.ts` — 6 tests via Vitest + Supertest)
  - Browser End-to-End Tests (`tests/e2e/dashboard.spec.ts` — Playwright E2E across all 9 dashboard modules)

---

## External Credentials & Key-Free Operation

Copy `.env.example` to `.env`:
```powershell
Copy-Item .env.example .env
```

**No paid API credentials are required to run core features.**
- **Works Out-of-the-Box Without Keys:**
  - Live HTTP Technical SEO / AEO / GEO Crawler against `https://www.incubrix.com` (`robots.txt`, `sitemap.xml`, `/llms.txt`, and all 13 public sitemap URLs)
  - 22 Prioritized Technical Fix Records + Automated JSON-LD / Patch Validator
  - 100 Validated Creator Questions + Non-Destructive Provenance Deduplicator
  - Documented Manual-Evidence Ingestion Workflow + Two-Pass AI Variance Verification Rule
  - Test-Mode Visibility Runs (`--mode test`)
  - 10 Publish-Ready Content Studio Pages + Automated Brief Generator + Markdown/HTML Exporter
  - 30 Verified Third-Party Citation Opportunities
  - Weekly Report Generator + 90-Day Launch Plan + Assessment Workbook Exporter
- **Optional Live Provider Keys (Configured in `.env`):**
  - `SERPAPI_API_KEY` or `GOOGLE_CSE_API_KEY` + `GOOGLE_CSE_CX` (Live automated Google SERP, Answer Box & AI Overview collection)
  - `OPENAI_API_KEY` (Live OpenAI ChatGPT adapter)
  - `GEMINI_API_KEY` (Live Google Gemini adapter)
  - `PERPLEXITY_API_KEY` (Live Perplexity Sonar citation adapter)
  - `ANTHROPIC_API_KEY` (Live Anthropic Claude adapter)

When an API key is not configured, the engine **never fabricates live results**; it marks unconfigured automated runs as `not_collected` and provides a documented manual-evidence workflow. Any demonstration simulation records are explicitly tagged `DEMO` (`is_demo = 1`) and strictly excluded from all official dashboard totals.

---

## CLI Engine Commands (`python -m engine.cli`)

```powershell
# Initialize DB, run live audit of incubrix.com, and generate all exports
python -m engine.cli init --live-audit

# Run live HTTP Technical SEO / AEO / GEO audit on incubrix.com
python -m engine.cli audit --target https://www.incubrix.com

# Run Visibility Engine in key-free test mode across US, India, and UK
python -m engine.cli run-visibility --mode test --markets US,IN,GB --limit 15

# Run Visibility Engine in live API mode (uses keys configured in .env)
python -m engine.cli run-visibility --mode live --markets US,IN,GB --limit 100 --pass-number 1

# Generate a new AEO/GEO Content Brief for any question ID
python -m engine.cli generate-brief --question-id Q-019 --content-type how_to_guide

# Generate Weekly Visibility Report (exports/weekly_visibility_report.md)
python -m engine.cli generate-report

# Export all CSVs and the Assessment Workbook Bundle (exports/workbook/)
python -m engine.cli export-all
```

---

## Windows Task Scheduler Guide (Weekly Automated Runs)

To schedule repeatable weekly data collection and reporting on Windows:

```powershell
$Action = New-ScheduledTaskAction -Execute "python" -Argument "-m engine.cli run-visibility --mode live --markets US,IN,GB --limit 100" -WorkingDirectory (Get-Location).Path
$Trigger = New-ScheduledTaskTrigger -Weekly -DaysOfWeek Monday -At 8am
Register-ScheduledTask -TaskName "IncuBrix-Weekly-Visibility-Engine" -Action $Action -Trigger $Trigger -Description "Weekly AEO/SEO/GEO multi-market visibility run"
```

---

## Running Automated Tests

```powershell
# Run Python Engine Unit Tests + TypeScript API/Zod Tests
npm test

# Run Playwright Browser E2E Suite across all 9 UI Sections
npm run test:e2e

# Run the entire verification suite (Python + Vitest + Playwright)
npm run test:all
```

---

## Key Real Findings from Live Inspection of `https://www.incubrix.com`

1. **Zero JSON-LD Structured Data (`ISS-001`, `ISS-003`, `ISS-004`, `ISS-007`, `ISS-008`):** All 13 sitemap pages on `incubrix.com` currently contain `0` `<script type="application/ld+json">` blocks. Ready-to-apply, validated `Organization`, `WebSite`, `SoftwareApplication` (6 pricing tiers: Free $0 to Pro $250/mo), `FAQPage`, `HowTo`, and `AboutPage` JSON-LD patches are generated in `data/patches/`.
2. **Missing `/llms.txt` (`ISS-002`):** `GET https://www.incubrix.com/llms.txt` returns `HTTP 404 Not Found`. A complete, factual `/llms.txt` file is generated in `data/patches/ISS-002.patch.txt`.
3. **Empty `<h1>` & Zero Internal Links on `/manifesto` (`ISS-005`, `ISS-006`):** `https://incubrix.com/manifesto` renders an empty `<h1></h1>` tag and has `0` internal navigation links back to core product pages.
4. **17 Content Images with Empty `alt=""` (`ISS-009`):** Found across `/` (1), `/about` (5), `/pricing` (5), and `/waitlist` (6).
5. **Missing Twitter/X Cards (`ISS-010`), Missing `<lastmod>` in `sitemap.xml` (`ISS-012`), Grammatical Typo & Pipe Character in Homepage Meta Description (`ISS-011`), and `/waitlist` Cannibalization (`ISS-016`).**

---

## Official Submission Package (`submission/`)

The finalized, validated submission bundle is organized in `submission/`:
- **`submission/workbook/`**: Official Excel workbook (`IncuBrix_2027_Growth_Engineer_Option_3_AEO_SEO_GEO_Submission_Workbook.xlsx`) plus tab CSVs.
- **`submission/visibility/`**: Official 100-row `visibility.csv`, `visibility_observations.csv`, and `REPRODUCIBILITY_AUDIT_REPORT.md` (Dual reproducibility audit: 94.9% repeat concordance, 100.0% data traceability).
- **`submission/evidence/`**: Raw crawled HTML files from `incubrix.com`, 127 raw observation JSON files, and 30 citation check files.
- **`submission/technical_fixes/`**: `TECHNICAL_SEO_AUDIT.md` and 22 candidate patch files (`patches/ISS-*.patch.txt`), plus 3 local implementations (`public/llms.txt`, `public/robots.txt`, `public/sitemap.xml`).
- **`submission/content_pages/`**: `CONTENT_QUALITY_REPORT.md` and 10 publish-ready pages in Markdown and HTML with valid JSON-LD and zero unverified roadmap claims.
- **`submission/citation_plan/`**: `CITATION_VALIDATION_REPORT.md`, `CITATION_TARGETS.csv`, `CITATION_OPPORTUNITY_REPORT.md`, and `citation_opportunities_30.csv` (Quality scoring: 89.2/100 average; 18 HTTP 200, 12 WAF-protected live domains).
- **`submission/reports/`**: 
  - `QUESTION_COVERAGE_REPORT.md` and `QUESTION_COVERAGE.csv` (100 questions, 7 categories, prioritized collection queue)
  - `OBSERVATION_COMPLETENESS_REPORT.md` (5 providers, 3 markets, 2 measurement days)
  - `TWO_PASS_COMPARISON_REPORT.md` (39 repeat pairs, 37 concordant, root cause analysis for 2 natural variance pairs)
  - `DATA_INTEGRITY_REPORT.md` (100% referential integrity, zero leaked secrets)
  - `FINAL_ASSESSMENT_READINESS_REPORT.md` (Master readiness scorecard)
  - `PROJECT_AUDIT.md`, `PRODUCT_MARKET_INSIGHTS.md`, `FINAL_TEST_REPORT.md`, `SUBMISSION_CHECKLIST.md`, and `weekly_visibility_report.md`
- **`submission/launch_kit/`**: `90_DAY_LAUNCH_KIT.md` and `06_launch_plan_90_days.csv` (12 weekly tasks across Days 1–30, 31–60, 61–90).
- **`submission/videos/`**: 5-minute product walkthrough script, 8-minute technical demo script, and video recording guide.

---

## Explicit Limitations & Governance

- **Live Website Non-Interference:** We do not own or administer `incubrix.com`. All 22 technical fixes are validated via automated unit tests against ready-to-apply patch artifacts (`data/patches/`); live production deployment on `incubrix.com` remains `0` until applied by the site owners.
- **No Unverified Claims:** Features marked *"Coming soon"* on `incubrix.com` (such as `/signal` Content Performance analytics and automated optimal-time scheduling) are explicitly flagged in Content Studio checklists rather than claimed as live.
- **Third-Party Citation Policy:** No third-party websites were modified or spammed, and no automated scraping was performed against restricted platforms.
