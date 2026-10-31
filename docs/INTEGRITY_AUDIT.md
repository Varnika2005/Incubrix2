# IncuBrix Visibility Engine — Comprehensive Codebase & Data Integrity Audit

**Audit Date:** `2026-10-25`  
**Target Property:** `https://www.incubrix.com` (Canonical Apex: `https://incubrix.com/`)  
**Database Inspected:** `data/incubrix.db` (SQLite WAL)  
**Scope:** End-to-end audit of repository files, SQLite schema (`engine/db.py`), metric calculation queries (`engine/reporting.py`), visibility pipeline (`engine/visibility.py`), technical auditor (`engine/auditor.py`), content studio (`engine/content_studio.py`), citation tracker (`engine/citations.py`), Express API (`server/index.ts`), CSV/Workbook exports (`exports/`), automated test suites (`tests/`), and documentation (`README.md`).

---

## 1. Executive Summary of Pre-Remediation State

Before remediation, the repository contained a mix of **genuine live HTTP crawl data** (the 13 crawled HTML pages from `https://incubrix.com` in `data/evidence/crawl/`) alongside **synthetic/illustrative baseline records and conflated status labels** that inflated official verified dashboard metrics:

| Deliverable / Metric | Pre-Remediation Displayed Value | Actual Underlying Source Record Reality | Integrity Classification |
| :--- | :--- | :--- | :--- |
| **Creator Questions** | `100 Validated` (`7` merged duplicates) | `106` raw questions in `engine/questions_seed.py` deduplicated via `normalize_question_fingerprint()` into `100` unique rows in `questions`. | **Valid (Curated Seed Dataset with Provenance)** |
| **AI Assistant Mention Rate** | `84.6%` (`22 / 26` AI observations) | Derived from `26` hardcoded Python strings in `seed_baseline_visibility_observations()` (`engine/visibility.py:630-825`) inserted with `is_demo = 0` and `collection_status = 'verified_observation'`. | **CRITICAL INTEGRITY DEFECT — Synthetic / Illustrative Strings Counted as Official Verified Observations** |
| **AI Assistant Citation Rate** | `76.9%` (`20 / 26` AI observations) | Same `26` hardcoded Python strings in `seed_baseline_visibility_observations()` (`engine/visibility.py:630-825`) with `is_demo = 0`. | **CRITICAL INTEGRITY DEFECT — Synthetic / Illustrative Strings Counted as Official Verified Observations** |
| **Google SERP Rankings** | `6 SERP Records (6 Ranked)` | Derived from `6` hardcoded tuples in `seed_baseline_visibility_observations()` (`Q-001`, `Q-005`, `Q-031` across two dates) rather than live SERP API responses. | **CRITICAL INTEGRITY DEFECT — Synthetic SERP Tuples Counted as Official Verified SERP Records** |
| **Technical SEO Audit Findings** | `22 Issues` across `13 Crawled Pages` | Backed by real HTTP GET requests to `https://incubrix.com/robots.txt`, `sitemap.xml`, `/llms.txt` (`HTTP 404`), and all `13` public URLs saved in `data/evidence/crawl/*.html`. | **Valid Live Crawl Findings** |
| **Technical Fixes Validated** | `22 Validated` (`validation_status = 'validated'`) | `validate_single_issue_patch()` (`engine/auditor.py:699-813`) validates the *candidate patch artifact* (`data/patches/ISS-*.patch.txt`), NOT whether the fix is deployed on live `https://incubrix.com`. | **HIGH INTEGRITY DEFECT — Candidate Patch Validation Conflated with Live Website Fix Validation** |
| **Citation Target URLs** | `30 Verified Live URLs` (`http_status_checked = 200`) | `seed_citation_opportunities()` (`engine/citations.py:524-579`) hardcoded `200` and `'verified_live'` for all 30 URLs without making HTTP requests or saving evidence files. | **HIGH INTEGRITY DEFECT — Hardcoded HTTP 200 Status Without Live Verification or Saved Evidence** |
| **Content Studio Pages** | `10 Publish-Ready Pages` (`7 ready_to_publish`, `2 reviewed`, `1 draft`) | `10` generated Markdown/HTML drafts in `engine/content_studio.py`. Three pages (`PAGE-001`, `PAGE-002`, `PAGE-003`) had non-empty `unverified_claims_flagged` arrays yet were marked `ready_to_publish`, and citation URLs inside pages were not live-checked. | **MEDIUM/HIGH INTEGRITY DEFECT — Generated Drafts & Pages with Flagged Claims Marked `ready_to_publish`** |
| **Gemini Live API Adapter** | Default model `gemini-2.5-flash` | Calling Google's `v1beta` endpoint with `gemini-2.5-flash` returns `HTTP 404: models/gemini-2.5-flash is no longer available to new users; use models/gemini-3.8-flash` (or `gemini-flash-latest`). | **HIGH FUNCTIONAL DEFECT — Outdated Default Gemini Model ID Causes Live API Calls to Fail with HTTP 404** |

---

## 2. Exact SQL Queries Traced for Every Overview Metric (`engine/reporting.py`)

Every metric returned by `GET /api/overview` (and rendered in `src/components/OverviewSection.tsx`) is computed in `compute_overview_metrics()` (`engine/reporting.py:258-473`):

### 2.1 Creator Questions (`metrics.questions`)
- `collected_total`:
  ```sql
  SELECT COUNT(*) AS c FROM questions WHERE is_demo = 0
  ```
- `validated_total`:
  ```sql
  SELECT COUNT(*) AS c FROM questions WHERE is_demo = 0 AND validation_status = 'validated'
  ```
- `duplicates_merged_with_provenance`:
  ```sql
  SELECT COALESCE(SUM(duplicate_merge_count), 0) AS c FROM questions WHERE is_demo = 0
  ```
- `questions_measured`:
  ```sql
  SELECT COUNT(DISTINCT question_id) AS c FROM visibility_observations
  WHERE is_demo = 0 AND collection_status IN ('verified_observation', 'pending_verification')
  ```
  - **Audit Finding:** Including `'pending_verification'` (single-pass unverified AI observations) in `questions_measured` and in AI mention/citation denominators violates strict separation between verified and unverified records.

### 2.2 Observation Collection States (`metrics.observation_states`)
- Query (`engine/reporting.py:278-280`):
  ```sql
  SELECT collection_status, COUNT(*) AS count FROM visibility_observations GROUP BY collection_status
  ```

### 2.3 Google Search Visibility (`metrics.search_visibility`)
- Query (`engine/reporting.py:300-306`):
  ```sql
  SELECT * FROM visibility_observations
  WHERE is_demo = 0 AND provider = 'google_search'
    AND collection_status IN ('verified_observation', 'pending_verification')
  ```
  - Python aggregations:
    - `google_records_count = len(google_obs)`
    - `google_ranked_count = sum(1 for r in google_obs if r["google_organic_rank"] is not None)`
    - `answer_box_count = sum(1 for r in google_obs if int(r["answer_box_present"]) == 1)`
    - `ai_overview_count = sum(1 for r in google_obs if int(r["ai_overview_present"]) == 1)`
    - `ai_overview_citing_incubrix = sum(1 for r in google_obs if int(r["ai_overview_cites_incubrix"]) == 1)`

### 2.4 AI Assistant Mention & Citation Rates (`metrics.ai_visibility`)
- Query (`engine/reporting.py:314-320`):
  ```sql
  SELECT * FROM visibility_observations
  WHERE is_demo = 0 AND provider IN ('chatgpt', 'gemini', 'perplexity', 'claude')
    AND collection_status IN ('verified_observation', 'pending_verification')
  ```
  - Numerator (Mentions): `ai_mentions = sum(1 for r in ai_obs if int(r["incubrix_mentioned"]) == 1)`
  - Numerator (Citations): `ai_citations = sum(1 for r in ai_obs if int(r["incubrix_cited"]) == 1)`
  - Denominator: `ai_total = len(ai_obs)`
  - **Audit Finding:**
    1. All 26 records in `ai_obs` came from `documented_cases` in `seed_baseline_visibility_observations()` (`engine/visibility.py:630-825`), which were hardcoded illustrative strings written in code rather than real API responses!
    2. `pending_verification` (single-pass) records (`Q-047`, `Q-096`) were included in both the numerator and denominator (`22 / 26 = 84.6%` and `20 / 26 = 76.9%`). Official verified rates must ONLY use `collection_status = 'verified_observation'` AND `is_demo = 0`.

### 2.5 Technical SEO Audit (`metrics.technical_audit`)
- Queries (`engine/reporting.py:376-386`):
  ```sql
  SELECT severity, COUNT(*) AS count FROM technical_issues GROUP BY severity;
  SELECT COUNT(*) AS c FROM technical_issues WHERE validation_status = 'validated';
  SELECT COUNT(*) AS c FROM crawled_pages;
  ```
  - **Audit Finding:** `run_live_website_audit()` (`engine/auditor.py:933-938`) sets `validation_status = 'validated'` whenever `validate_single_issue_patch(issue)` passes on the local patch text (`data/patches/ISS-*.patch.txt`), even though the live page on `https://incubrix.com` still exhibits the defect!

### 2.6 Content Studio (`metrics.content_studio`)
- Query (`engine/reporting.py:389-391`):
  ```sql
  SELECT status, COUNT(*) AS count FROM content_pages GROUP BY status
  ```

### 2.7 Citation Opportunities (`metrics.citations`)
- Queries (`engine/reporting.py:398-401`):
  ```sql
  SELECT COUNT(*) AS c FROM citation_opportunities;
  SELECT COUNT(*) AS c FROM citation_opportunities WHERE verification_status = 'verified_live';
  ```

---

## 3. Traceability of Every Displayed Record Type

### 3.1 Visibility Observations (`visibility_observations` table)
- **Pre-Remediation Records (`39` total rows):**
  - `30` rows (`OBS-Q-001-...` to `OBS-Q-089-...`): Hardcoded in `engine/visibility.py:630-811` (`seed_baseline_visibility_observations`), saved to `data/evidence/observations/OBS-*.json` with `is_demo = 0` and `collection_status = 'verified_observation'`. **Reality:** These are synthetic/illustrative baseline scenarios authored in Python, NOT live API responses.
  - `2` rows (`OBS-Q-047-...`, `OBS-Q-096-...`): Hardcoded single-pass strings in `engine/visibility.py:813-825` with `is_demo = 0` and `collection_status = 'pending_verification'`. **Reality:** Also synthetic strings.
  - `3` rows (`Q-002`, `Q-003`, `Q-004`): `not_collected` status records.
  - `2` rows (`Q-019`, `Q-021`): Seeded `failed_collection` examples (`TimeoutError` and `HTTPError 429`).
  - `2` rows (`OBS-DEMO-Q-010-...`, `OBS-DEMO-Q-032-...`): Explicitly labelled `is_demo = 1`, `collection_status = 'demo_observation'`.

### 3.2 Technical SEO Issues (`technical_issues` & `crawled_pages` tables)
- **Crawled Pages (`13` rows in `crawled_pages` + `data/evidence/crawl/*.html`):**
  - **Reality:** **100% Real HTTP Crawl Observations.** Crawled live from `https://incubrix.com` (`index.html`, `about.html`, `how-it-works.html`, `pricing.html`, `contact.html`, `waitlist.html`, `faq.html`, `team.html`, `privacy.html`, `terms.html`, `manifesto.html`, `careers.html`, `investors.html`, plus `robots.txt`).
- **Technical Issues (`ISS-001` through `ISS-022` in `technical_issues`):**
  - **Reality:** Every finding (`0` JSON-LD blocks across all 13 pages, `HTTP 404` on `/llms.txt`, empty `<h1></h1>` and `0` internal links on `/manifesto`, `17` images missing `alt` attributes across `/`, `/about`, `/pricing`, `/waitlist`, missing Twitter Card meta tags, missing `<lastmod>` in `sitemap.xml`, etc.) is verified directly against the saved raw HTML in `data/evidence/crawl/`.
  - **Defect:** Their `validation_status` was set to `'validated'` based on validating the local patch file (`data/patches/ISS-*.patch.txt`) rather than validating against the live HTML of `https://incubrix.com`.

### 3.3 Content Studio Pages (`content_pages` table & `exports/content_pages/`)
- **Records (`PAGE-001` through `PAGE-010`):**
  - **Reality:** Generated AEO/GEO drafts stored in `engine/content_studio.py` and exported to `exports/content_pages/*.md` and `*.html`.
  - **Defect:** `7` pages were seeded with `status = 'ready_to_publish'` and `2` as `'reviewed'`, including `PAGE-001`, `PAGE-002`, and `PAGE-003` which explicitly contain `unverified_claims_flagged` entries requiring human review. Furthermore, OverviewSection labelled all `10` total pages as `"Publish-Ready AEO/GEO Pages"`.

### 3.4 Citation Opportunities (`citation_opportunities` table)
- **Records (`CIT-001` through `CIT-030`):**
  - **Reality:** Curated list of 30 real third-party URLs (`g2.com`, `capterra.com`, `producthunt.com`, `alternativeto.net`, `trustradius.com`, `futurepedia.io`, `theresanaiforthat.com`, `buffer.com`, `sproutsocial.com`, `later.com`, `creators.spotify.com`, `reddit.com`, `indiehackers.com`, `news.ycombinator.com`, `getapp.com`, `softwareadvice.com`, `llmstxt.org`).
  - **Defect:** `seed_citation_opportunities()` hardcoded `http_status_checked = 200` and `verification_status = 'verified_live'` without performing live HTTP checks or storing response evidence in `data/evidence/citations/`.

---

## 4. Detailed Issue List, Severity & Remediation Plan

| Issue ID | Severity | Affected File(s) & Lines | Description of Integrity / Functional Issue | Remediation Action |
| :--- | :--- | :--- | :--- | :--- |
| **AUD-01** | **CRITICAL** | `engine/visibility.py:577-925`<br>`engine/reporting.py:292-364` | `seed_baseline_visibility_observations()` inserts 32 hardcoded synthetic/illustrative responses (`documented_cases`) with `is_demo = 0` and `collection_status = 'verified_observation'` (or `'pending_verification'`), inflating official AI mention rate to `84.6%`, citation rate to `76.9%`, and Google SERP ranked records to `6`. | 1. Reclassify all synthetic seeded scenarios as `is_demo = 1` and `collection_status = 'demo_observation'` so they are preserved for demonstration/investigation but **100% excluded from official metrics**.<br>2. In `compute_overview_metrics()`, compute official verified rates strictly from `WHERE is_demo = 0 AND collection_status = 'verified_observation'`. |
| **AUD-02** | **HIGH** | `engine/visibility.py:63,218` | Default Gemini model is hardcoded to `gemini-2.5-flash`, which Google's API rejects for new keys with `HTTP 404` (`use models/gemini-3.8-flash` or `gemini-flash-latest`). Meanwhile, a real `GEMINI_API_KEY` is present in the environment and succeeds with `gemini-flash-latest`! | Update default Gemini model to `gemini-flash-latest` (with automatic fallback across `gemini-flash-latest` and `gemini-2.5-flash-lite`) so real live Gemini API calls succeed across US, IN, and GB across 2 passes and 2 runs! |
| **AUD-03** | **HIGH** | `engine/auditor.py:699-983`<br>`engine/reporting.py:383-385,448` | `technical_issues.validation_status` is set to `'validated'` when the candidate patch file passes syntax checks, conflating local patch validation with live website validation on `incubrix.com`. | 1. Add `validate_issue_against_live_site(issue, crawled_signals)` to test whether each issue is actually resolved on the live crawled HTML.<br>2. Set `validation_status = 'patch_tested_pending_deploy'` when the local patch passes validation (`22/22`) while the live site still has the defect (`live_validated = 0`), and only set `validation_status = 'validated'` if verified fixed on the target HTML. |
| **AUD-04** | **HIGH** | `engine/citations.py:524-580` | All 30 citation URLs are seeded with `http_status_checked = 200` and `verification_status = 'verified_live'` without real HTTP checks or saved evidence files in `data/evidence/citations/`. | Implement `verify_citation_opportunities_live()` to perform real HTTP requests to all 30 URLs, save `data/evidence/citations/CIT-XXX.json` with HTTP status, final URL, `<title>`, and timestamp, and mark `verified_live` **only** when HTTP 200 is actually returned (marking `403`/`429` bot-protected pages as `http_restricted_unverified` or `pending_check`). |
| **AUD-05** | **MEDIUM** | `engine/content_studio.py:36-76,873-945`<br>`src/components/OverviewSection.tsx:325` | Content Studio pages with non-empty `unverified_claims_flagged` (`PAGE-001`, `PAGE-002`, `PAGE-003`) are marked `ready_to_publish`, and `validate_content_page()` does not check internal link target validity or claim flag status when assigning `ready_to_publish`. | Update `validate_content_page()` and `seed_content_pages()` so any page with `unverified_claims_flagged` is restricted to `'draft'` (or `'reviewed'` awaiting claim removal), verify all internal links against known valid `incubrix.com` routes, and update Overview labels to distinguish total drafts (`10`) from strictly verified publish-ready pages (`6`). |
| **AUD-06** | **MEDIUM** | `engine/cli.py:49,96,123`<br>`server/index.ts:587-601` | Phase 4 requires exporting `exports/visibility.csv` with traceable evidence references, whereas CLI only wrote `exports/visibility_observations.csv`. | Update `export_visibility_to_csv()` and `engine/cli.py` to write both `exports/visibility.csv` and `exports/visibility_observations.csv` with full evidence path, provider, location setting, pass number, and timestamp columns. |
| **AUD-07** | **MEDIUM** | `engine/visibility.py:311-385`<br>`tests/python/test_engine_suite.py` | Provider adapter needs explicit handling and unit tests for HTTP 429 rate limits, malformed JSON responses, empty datasets, and idempotent refreshes ensuring failed or single-pass records are never promoted to `verified_observation` on refresh. | Add explicit `urllib.error.HTTPError` (429/5xx) and `json.JSONDecodeError` handling in `call_live_provider_adapter()`, ensure `execute_visibility_run()` never promotes failed/single-pass records on refresh, and add unit tests covering all edge cases. |
