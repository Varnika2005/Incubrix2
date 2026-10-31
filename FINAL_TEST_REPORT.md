# IncuBrix AEO / SEO / GEO Visibility Engine — Final Automated Test Report

**Execution Timestamp:** October 31, 2026 (Live Run)  
**Target Environment:** Windows 11 PowerShell (`d:\incubrix2`)  
**Node.js Version:** `v22.17.1`  
**Python Version:** `3.10.11`  
**Database:** Local SQLite (`./data/incubrix.db` WAL mode)  
**Overall Result:** **14 / 14 TESTS PASSED (100% SUCCESS RATE, ZERO FAILURES)**  
**Reproducibility Audit:** **20 / 20 MATCHES (100.0%, TARGET: >= 85%)**  
**Production Build:** **SUCCESS (Vite 6.4.5, 6.90s)**  

---

## 1. Test Execution Summary

| Test Framework / Level | Test File / Command | Tests Run | Passed | Failed | Skipped | Duration |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: |
| **Python Engine Unit & Integration** | `tests/python/test_engine_suite.py` | 7 | **7** | 0 | 0 | 1.066s |
| **Node.js Express API & Zod Schemas** | `tests/unit/api.test.ts` (Vitest) | 6 | **6** | 0 | 0 | 0.459s |
| **Browser End-to-End Navigation** | `tests/e2e/dashboard.spec.ts` (Playwright) | 1 (9 steps) | **1** | 0 | 0 | 4.6s (10.5s total) |
| **Reproducibility Audit Suite** | `engine/run_reproducibility_audit.py` | 20 | **20** | 0 | 0 | 0.280s |
| **Production Vite Build** | `npm run build` | 1 | **1** | 0 | 0 | 6.90s |
| **Idempotent Tracker CLI (Test Mode)**| `python -m engine.cli run-visibility` | 1 | **1** | 0 | 0 | 0.006s |
| **Combined Full Suite** | `npm run test:all` | **14** | **14** | **0** | **0** | **~12s** |

---

## 2. Python Engine Test Suite Details (`tests/python/test_engine_suite.py`)

Run Command: `python -m unittest discover -s tests/python -p "test_*.py" -v`

### Test 1: `test_question_deduplication_preserves_provenance`
- **Result:** `PASS (ok)`
- **Actual Output:** Normalized semantic fingerprints across 106 raw questions to produce 100 canonical creator questions. Preserved 6 duplicate variants with original wording and source URLs in `provenance_sources_json`.

### Test 2: `test_visibility_calculations_and_two_pass_verification`
- **Result:** `PASS (ok)`
- **Actual Output:** Single-pass observation correctly stored as `pending_verification`. Running Pass 2 promoted status to `verified_observation`. Verified that `is_demo = 1` rows are cleanly filtered out from official metrics.

### Test 3: `test_missing_failed_observations_and_provider_edge_cases`
- **Result:** `PASS (ok)`
- **Actual Output:** Missing provider API keys correctly return `not_collected`. Simulated 429 rate limit correctly returns `failed_collection` with error message, without crashing.

### Test 4: `test_multi_date_comparisons_and_idempotent_rerun`
- **Result:** `PASS (ok)`
- **Actual Output:** Compared observations across Day 1 (2026-10-24) and Day 2 (2026-10-25). Rerunning `seed_baseline_visibility_observations` twice produced identical observation counts without duplicates.

### Test 5: `test_csv_import_and_export`
- **Result:** `PASS (ok)`
- **Actual Output:** Exported `questions.csv` (100 rows) and `visibility.csv` (100 rows). Re-importing into database merged all 100 questions cleanly without creating duplicates.

### Test 6: `test_technical_audit_rules_and_json_ld_validation`
- **Result:** `PASS (ok)`
- **Actual Output:** HTML parser correctly flagged missing `<h1>`, missing image `alt`, and missing canonical links. `validate_json_ld()` rejected fabricated `AggregateRating` / `reviewCount` schema, enforcing honesty. Verified all 22 candidate patch artifacts while `live_fixes_validated == 0`.

### Test 7: `test_content_studio_validation_and_report_generation`
- **Result:** `PASS (ok)`
- **Actual Output:** Validated all 10 publish-ready content pages. Confirmed that flagging unverified roadmap claims blocks publication. Successfully generated weekly report and workbook export bundle.

---

## 3. Node.js Vitest API Test Suite Details (`tests/unit/api.test.ts`)

Run Command: `npx vitest run`

1. `GET /api/overview` — returns genuine SQLite metrics with `is_demo=0` separation. (`PASS`)
2. `GET /api/questions` — returns 100 creator questions with category and intent filtering. (`PASS`)
3. `POST /api/visibility/manual` — validates Zod schema, records observation, saves evidence JSON, enforces two-pass rule. (`PASS`)
4. `GET /api/audit` — returns 22 prioritized technical issues with `live_fixes_validated: 0` and `patch_artifacts_validated: 22`. (`PASS`)
5. `GET /api/content` — returns 10 publish-ready pages with 0 unverified claims. (`PASS`)
6. `GET /api/citations` — returns 30 citation opportunities with live HTTP status codes. (`PASS`)

---

## 4. Playwright End-to-End Browser Test Suite (`tests/e2e/dashboard.spec.ts`)

Run Command: `npx playwright test`

- **Execution:** Chromium headless browser on `http://localhost:3000`.
- **Navigation Flow Verified:**
  1. Overview Dashboard loads real SQLite counters.
  2. Question Repository displays 100 questions with search and filter.
  3. Visibility Matrix displays multi-provider / multi-market grids.
  4. Manual Evidence Ingestion modal opens and validates inputs.
  5. Technical SEO Audit lists 22 prioritized candidate patches.
  6. Content Studio lists 10 publish-ready pages.
  7. Citation Opportunity Manager lists 30 targets.
  8. Weekly Report view renders Markdown analysis and recommendations.
  9. 90-Day Launch Kit renders weekly roadmap with owners, budgets, and milestones.
- **Result:** `1 passed (4.6s test, 10.5s total process)`.

---

## 5. 20-Sample Independent Reproducibility Audit

Run Command: `python -m engine.run_reproducibility_audit`

- **Sample Size:** 20 creator questions (pseudo-randomly sampled with seed `42`).
- **Matches:** **20 / 20** (100.0%).
- **Mismatches:** **0**.
- **Target:** $\ge 85\%$.
- **Result:** **PASSED (100.0%)**.

---

## 6. Tracker CLI Test Mode & Idempotency Verification

Run Command: `python -m engine.cli run-visibility --mode test --limit 15`

```json
{
  "run_id": "RUN-VIS-1793466833400",
  "mode": "test",
  "questions_targeted": 15,
  "observations_recorded": 225,
  "verified_count": 0,
  "failed_count": 0,
  "skipped_unavailable_count": 225,
  "duration_ms": 6,
  "estimated_cost_usd": 0.0
}
```
- **Verified Observations in DB before run:** 36
- **Verified Observations in DB after run:** 36 (100% preserved, zero corruption)

---

## 7. Production Build Verification

Run Command: `npm run build`
- **Bundler:** Vite v6.4.5
- **Modules Transformed:** 2,218 modules
- **Output Artifacts:**
  - `dist/index.html` (1.06 kB)
  - `dist/assets/index-*.css` (38.04 kB)
  - `dist/assets/index-*.js` (726.39 kB)
- **Status:** **SUCCESS (built in 6.90s)**
