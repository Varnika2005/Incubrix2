# IncuBrix AEO/SEO/GEO Engine — README Execution Validation Guide

**Target Property:** `https://www.incubrix.com` (Canonical Apex: `https://incubrix.com/`)  
**Assessment Requirement:** Priority 3 / Option 3: Rerunnable from README by an Independent Evaluator  
**Audit Date:** `2026-10-31` / `2026-11-01`  
**Execution Environment Tested:** Windows 11 PowerShell, Node.js v20+, Python 3.11+, SQLite 3  

---

## 1. Executive Summary & Reproducibility Guarantee

- **Reproducibility Status:** **100% PASS** — Zero machine-specific hardcoded absolute paths, zero required paid external API dependencies for evaluation.
- **Single-Command Quickstart:** Tested and confirmed operational via `npm run setup` followed by `npm start`.
- **Key-Free Execution:** All 9 dashboard sections, the live HTTP crawler, automated technical validators, question deduplicator, 10 publish-ready content pages, and 30 citation targets run out of the box without any paid API keys.
- **Automated Tests:** 16/16 automated unit/integration tests pass in < 2 seconds (`npm test`).
- **Production Build:** `npm run build` succeeds in < 6 seconds generating production bundle in `dist/`.

---

## 2. Step-by-Step Evaluator Walkthrough

### Step 1: Clone Repository & Install Dependencies
```bash
# Clone the repository
git clone <repository-url> incubrix
cd incubrix

# Install Node.js packages
npm install
```

### Step 2: Environment Configuration (Optional)
```bash
# Copy example configuration (No paid keys required for core execution)
cp .env.example .env
```
*Note: If you have a Google Gemini API key or OpenAI key, you can add them to `.env`. When keys are unconfigured, the engine transparently runs in key-free test/benchmark mode (`--mode test`) and never synthesizes fake answers.*

### Step 3: Run Database Initialization & Live Website Audit
```bash
# Initialize SQLite database, crawl incubrix.com, validate 22 patches,
# seed 100 creator questions, 10 content pages, and 30 citation targets:
npm run setup
```
**Expected Output:**
```
1. Initialized SQLite database (data/incubrix.db)
2. Live crawled 13 sitemap URLs on https://www.incubrix.com
3. Validated 22 technical SEO/AEO/GEO patches (100% pass)
4. Seeded 100 creator questions across 7 categories
5. Validated 10 publish-ready content pages (100% ready_to_publish)
6. Validated 30 citation opportunities (18 HTTP 200, 12 WAF-protected)
7. Exported all assessment CSV files to exports/
```

### Step 4: Run Automated Tests
```bash
npm test
```
**Expected Output:**
```
> incubrix-visibility-engine@1.0.0 test
> npm run test:python && npm run test:unit

Ran 9 tests in 1.150s: OK
✓ tests/unit/api.test.ts (7 tests)
Test Files  1 passed (1)
Tests  16 passed (16)
```

### Step 5: Start Backend API & React Dashboard
```bash
npm start
```
- **Backend API:** `http://localhost:3001` (Health check: `http://localhost:3001/api/health`)
- **React Frontend:** `http://localhost:5173` (Light-theme editorial analytics dashboard)

---

## 3. CLI Engine Commands Quick Reference

Evaluators can run individual engine modules directly via Python:

| Command | Purpose | Expected Result |
| :--- | :--- | :--- |
| `python -m engine.cli init --live-audit` | Re-initialize database & crawl live site | Full refresh of `incubrix.db` |
| `python -m engine.cli run-visibility --mode test --limit 5` | Run key-free test visibility query | JSON run summary in < 50ms |
| `python -m engine.cli run-visibility --mode live --limit 5` | Run live AI visibility query (uses `.env` keys) | Live model responses & JSON evidence |
| `python -m engine.cli generate-brief --question-id Q-019` | Generate AEO content brief | Structured JSON brief output |
| `python -m engine.cli generate-report` | Generate weekly markdown report | `exports/weekly_visibility_report.md` |
| `python -m engine.cli export-all` | Export all CSVs & workbook support files | Synchronized files in `exports/` |

---

## 4. Production Build Verification

To verify that the application compiles cleanly for production hosting:
```bash
npm run build
```
**Expected Output:**
```
✓ 2218 modules transformed.
dist/index.html                   1.06 kB
dist/assets/index-CSJC0yGe.css   38.07 kB
dist/assets/index-BQAVJAh-.js   727.49 kB
✓ built in 5.72s
```

---

## 5. Troubleshooting Common Issues

1. **Port Conflicts (`EADDRINUSE: 3001` or `5173`):**
   - The Express server defaults to port `3001` (or `process.env.PORT`). If occupied, run:
     ```powershell
     Stop-Process -Id (Get-NetTCPConnection -LocalPort 3001).OwningProcess -Force
     ```
2. **Missing Python Modules:**
   - The engine uses standard library modules (`sqlite3`, `urllib.request`, `json`, `xml.etree.ElementTree`, `unittest`). No pip dependencies are required for the core Python CLI engine.
3. **OpenAI Quota Limit (`insufficient_quota`):**
   - If your OpenAI API key has zero credits, the engine catches the error, leaves existing evidence intact, and provides the documented manual research workflow.
