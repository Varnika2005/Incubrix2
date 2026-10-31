# INCUBRIX AEO / SEO / GEO VISIBILITY ENGINE — LIVE DEMO STATUS

**Session Timestamp:** October 31, 2026  
**Demonstration Mode:** LIVE & ACTIVE  
**Primary Target:** `https://incubrix.com/` (`https://www.incubrix.com`)  
**Status:** **ONLINE, REACHABLE & ALL 9 MODULES FULLY OPERATIONAL**

---

## 1. Live Application Endpoints

| Component | URL | Status | Description |
| :--- | :--- | :---: | :--- |
| **Frontend Dashboard (Dev)** | `http://localhost:5173/` | **ACTIVE** | Vite React 19 UI with hot-reload and Tailwind CSS v4 |
| **Frontend Single-Port (Prod)**| `http://localhost:3001/` | **ACTIVE** | Express static SPA hosting from `dist/` |
| **Backend Express API** | `http://localhost:3001/api` | **ACTIVE** | Node.js Express server + SQLite WAL database connection |
| **API Health Check** | `http://localhost:3001/api/health` | **HTTP 200** | Returns system timestamp and target property |

---

## 2. Server & Database State

- **Process Status:** Concurrently running backend (`dev:api` on port `3001`) and frontend (`dev:web` on port `5173`).
- **Database Engine:** Node.js native `DatabaseSync` (`node:sqlite`) with WAL (Write-Ahead Logging) mode.
- **Database Path:** `data/incubrix.db` (cleanly backed up to `data/incubrix.db.sprint_backup`).
- **Database Content:**
  - `questions`: 100 canonical creator questions (100% with documented source provenance).
  - `visibility_observations`: 36 genuine 2-pass verified Gemini observations, 1 pending observation, honest `not_collected` / `failed_collection` states, and demo records strictly isolated (`is_demo = 1`).
  - `technical_issues`: 22 prioritized issues with ready-to-paste `.patch.txt` files (`ISS-001` to `ISS-022`).
  - `content_pages`: 10 publish-ready pages (Markdown & HTML, answer-first, 0 unverified claims).
  - `citation_opportunities`: 30 targets (18 Live HTTP 200, 12 WAF Protected HTTP 403).
  - `launch_plan_tasks`: 12 weekly implementation activities across Month 1, 2, and 3.

---

## 3. Operational Status of All Nine Dashboard Modules

| # | Module Name | UI TestID / Nav | Status | Real Data Source |
| :-: | :--- | :--- | :---: | :--- |
| 1 | **Overview Dashboard** | `overview-section` | **ACTIVE** | Live counters from `GET /api/overview` (100 questions, 22 issues, 10 pages, 30 citations). |
| 2 | **Research Questions** | `questions-section` | **ACTIVE** | Searchable table of 100 questions, search intents, priority scores, and provenance URLs. |
| 3 | **Visibility Tracker** | `visibility-section` | **ACTIVE** | Multi-market grid (US, IN, GB) across Google Search and 4 AI assistants with two-date comparison. |
| 4 | **Manual Evidence Ingestion**| Modal in Visibility | **ACTIVE** | `POST /api/visibility/manual` parses raw responses, citations, competitors, and enforces 2-pass rule. |
| 5 | **Technical SEO Audit** | `audit-section` | **ACTIVE** | 22 prioritized fixes with code snippets and interactive JSON-LD validator testing. |
| 6 | **Content Studio** | `content-section` | **ACTIVE** | 10 publish-ready pages with interactive 2-sentence Direct Answer Brief Generator. |
| 7 | **Citation Opportunities** | `citations-section` | **ACTIVE** | 30 targets with live HTTP status badges, authority metrics, and earning angles. |
| 8 | **Weekly Reports** | `reports-section` | **ACTIVE** | Markdown report viewer with self-check verification and CSV export downloads. |
| 9 | **Launch Plan & Settings** | `launch-section` | **ACTIVE** | 90-day roadmap with owners/budgets and 5 search/AI provider adapter indicators. |

---

## 4. Recommended 4-Minute Live Interview Demonstration Workflow

Follow this sequence to showcase technical competence, assessment compliance, and system integrity:

```
Step 1: Overview & Integrity Rules (45 seconds)
  → Open http://localhost:5173/ in the browser.
  → Point out the 4 top KPI cards (100 Questions, 22 Issues, 10 Pages, 30 Citations).
  → Highlight the badge: "DEMO Records Strictly Excluded from Totals" — explaining your anti-fabrication architecture.

Step 2: Visibility Baseline & Multi-Pass Verification (60 seconds)
  → Click "Visibility Tracker" in the sidebar.
  → Point to the 36 verified observations collected via Google Gemini across US, IN, and GB markets on Oct 24 & Oct 25.
  → Explain the Two-Pass Verification Rule: an AI answer is only marked 'verified' when checked at least twice on disk.
  → Show the "Manual Evidence Ingestion" button: explain how non-automated providers (ChatGPT, Claude) can be imported with instant citation and competitor extraction.

Step 3: Technical SEO & Schema Validator (45 seconds)
  → Click "Technical SEO" in the sidebar.
  → Show ISS-001 (Missing Organization/WebSite JSON-LD) and ISS-002 (Missing /llms.txt).
  → Click the "Validate JSON-LD" interactive button: demonstrate real-time Schema.org validation enforcing zero fabricated ratings/reviews.
  → State honestly: 22 candidate patches are validated in data/patches/, and 0/22 are deployed to production without client authorization.

Step 4: Content Studio & Brief Generator (45 seconds)
  → Click "Content Studio" in the sidebar.
  → Show the 10 publish-ready pages; highlight that all 10 have 0 unverified roadmap claims and follow Answer-First structure.
  → Click "Generate Brief" on PAGE-001: show the instant 2-sentence direct answer draft structured for Google Answer Box and AI Overviews.

Step 5: Citations, Reports & Export Actions (45 seconds)
  → Click "Citations": explain the 18 Live (HTTP 200) vs 12 WAF Protected (HTTP 403) platforms (e.g. Product Hunt Cloudflare defense).
  → Click "Reports": show the generated weekly visibility report.
  → Click "Export CSV" to trigger an instant download of visibility.csv (100 rows matching official workbook sheet 02_QUESTIONS).
```

---

## 5. Known Operational Limitations & Honest Disclosures

1. **API Key Integration Status:**
   - **Google Gemini:** Configured and **100% LIVE** (`gemini-3.5-flash-lite`). Real-time live inference verified.
   - **OpenAI ChatGPT:** Configured in `.env`. Key is authenticated, but currently returns HTTP 429 (`credit_balance_exhausted: You have no credits remaining. Add credits to continue using the API`).
   - **Anthropic, Perplexity & SerpApi:** Unconfigured in `.env`; queries are tracked transparently as `not_collected`.
2. **Production Deployment:** Candidate patches are provided in `data/patches/ISS-*.patch.txt` and ready to paste; candidate does not have SSH/DNS/CMS access to `https://incubrix.com/`.
3. **Application Lifecycle:** The application is running in the background and will remain active on `http://localhost:5173/` and `http://localhost:3001/` throughout your demonstration.

