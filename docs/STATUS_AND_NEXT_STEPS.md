# IncuBrix Visibility Engine — Status, Verified Deliverables & Next Steps

**Target Website:** `https://www.incubrix.com` (Canonical: `https://incubrix.com/`)  
**Audit & Verification Date:** `2026-10-25`  
**Related Audit Document:** [`docs/INTEGRITY_AUDIT.md`](./INTEGRITY_AUDIT.md)

---

## 1. What Works & Supporting Automated Tests

Every module of the **IncuBrix AEO / SEO / GEO Visibility Engine** has been audited, remediated to remove unverified or synthetic claims from official metrics, and verified end-to-end.

### Automated Test Suites (All Passing)

| Test Suite | Command | File | Status | What It Verifies |
| :--- | :--- | :--- | :--- | :--- |
| **Python Engine Unit & Integration Suite (7 tests)** | `npm run test:python` (`python -m unittest discover -s tests/python -p "test_*.py" -v`) | [`tests/python/test_engine_suite.py`](../tests/python/test_engine_suite.py) | **PASS (`7/7` in `1.09s`)** | 1. `test_question_deduplication_preserves_provenance`: Normalizes fingerprints, merges duplicate questions (`106 -> 100`), and preserves all source URLs/wordings in `provenance_sources_json`.<br>2. `test_visibility_calculations_and_two_pass_verification`: Verifies that a single AI pass (`pass_number = 1`) stays `pending_verification` and is excluded from official rates until `pass_number = 2` is recorded with saved disk evidence; confirms `DEMO` rows (`is_demo = 1`) are excluded from official totals.<br>3. `test_missing_failed_observations_and_provider_edge_cases`: Tests missing API keys (`not_collected`), socket `TimeoutError` (`failed_collection`), `HTTP 429` rate limit (`failed_collection`), malformed JSON (`MalformedJSONError` -> `failed_collection`), and empty response payload (`EmptyResponseError` -> `failed_collection`).<br>4. `test_multi_date_comparisons_and_idempotent_rerun`: Confirms `compare_observations_across_dates` compares only `verified_observation` (`is_demo = 0`) pairs across distinct dates, and confirms repeated `execute_visibility_run` calls neither duplicate rows nor falsely promote `failed_collection`/`pending_verification` rows.<br>5. `test_csv_import_and_export`: Exports `questions.csv` (`100` rows) and `visibility.csv` (`47` non-demo rows) and re-imports `questions.csv` idempotently (`0` duplicates).<br>6. `test_technical_audit_rules_and_json_ld_validation`: Tests `parse_html_signals`, confirms `validate_json_ld` rejects fabricated `AggregateRating`/`review` properties, and verifies `live_fixes_validated == 0` vs `patch_artifacts_validated == 22`.<br>7. `test_content_studio_validation_and_report_generation`: Confirms `validate_content_page` blocks any page with non-empty `unverified_claims_flagged` from `ready_to_publish`, validates internal links against `DEFAULT_SITEMAP_URLS`, generates briefs, and verifies the 6-tab workbook bundle. |
| **Backend API & Zod Validation Suite (6 tests)** | `npm run test:unit` (`vitest run`) | [`tests/unit/api.test.ts`](../tests/unit/api.test.ts) | **PASS (`6/6` in `1.28s`)** | Tests `GET /api/health`, `GET /api/overview`, `GET /api/questions` (and category filtering), `POST /api/questions` (Zod validation + duplicate provenance merging), `GET /api/audit`, `POST /api/audit/validate-jsonld` (rejecting fake `AggregateRating`), `GET /api/content`, `GET /api/citations`, `GET /api/reports`, and `GET /api/launch-plan`. |
| **Playwright E2E Browser Suite (1 full-journey test)** | `npm run test:e2e` (`playwright test`) | [`tests/e2e/dashboard.spec.ts`](../tests/e2e/dashboard.spec.ts) | **PASS (`1/1` in `5.2s`)** | Launches the Express + Vite application, verifies SQLite KPIs rendered on the Overview dashboard, navigates across all 9 modules (`Overview`, `Visibility Tracker`, `Technical SEO Audit`, `Content Studio`, `Citation Opportunities`, `Research Questions`, `Reports`, `Launch Plan`, `Settings`), runs the interactive JSON-LD validator, and tests the Content Brief generator. |

---

## 2. Verified Counts for Every Deliverable

All numbers below are queried directly from `data/incubrix.db` via `compute_overview_metrics()` in [`engine/reporting.py`](../engine/reporting.py):

| Deliverable | Official Verified Count | Supporting Breakdown & Status Labels |
| :--- | :--- | :--- |
| **1. Creator Questions Collected & Validated** | **100 / 100 Validated** | `106` raw questions ingested -> `100` unique canonical questions across 7 categories (`15` Content Creation, `15` AI Video Editing, `15` Content Repurposing, `14` Captioning & Voiceovers, `14` Multi-Platform Publishing, `14` Creator Growth & Analytics, `13` Product Comparisons) + `6` duplicate variants merged into `provenance_sources_json`. All `100` have permitted source URLs and original wording. |
| **2. Search & AI Visibility Observations** | **36 Verified Observations** (`18` 2-pass pairs) | - **`36` `verified_observation`**: Genuine 2-pass live `gemini-3.5-flash-lite` API responses across `US` (`en-US`), `IN` (`en-IN`), and `GB` (`en-GB`) collected across two dates (`2026-10-24` and `2026-10-25`) with raw API JSON saved in `data/evidence/observations/OBS-*.json`.<br>- **`1` `pending_verification`**: Genuine 1-pass live `gemini-3.5-flash-lite` response (`Q-047`, `US`, Pass 1 only) held in pending until Pass 2 is run.<br>- **`8` `not_collected`**: Honest records where paid API keys (`OPENAI_API_KEY`, `PERPLEXITY_API_KEY`, `ANTHROPIC_API_KEY`, `SERPAPI_API_KEY`) are not configured.<br>- **`2` `failed_collection`**: Rate-limit (`HTTP 429`) and timeout (`15000ms`) error records.<br>- **`34` `demo_observation` (`DEMO`)**: `32` baseline demonstration scenarios (`OBS-DEMO-Q-*.json`) + `2` sandbox examples, strictly excluded from all official rates and totals. |
| **3. Official AI Mention & Citation Rates** | **38.9% Mention Rate** (`14 / 36`)<br>**0.0% Citation Rate** (`0 / 36`) | Computed strictly over the `36` verified 2-pass live Gemini API observations (`is_demo = 0`, `collection_status = 'verified_observation'`). IncuBrix is mentioned on brand/CreatorOps comparative queries (`Q-001`, `Q-088`, `Q-089`) and has `0%` unprompted visibility on generic category queries (`Q-005`, `Q-016`, `Q-017`, `Q-031`, `Q-060`). Standard ungrounded `gemini-3.5-flash-lite` outputs `0` URL citations (`0.0%`). |
| **4. Official Google SERP & AI Overview Records** | **0 Verified Live SERP Records** | Neither `SERPAPI_API_KEY` nor `GOOGLE_CSE_API_KEY` is configured in the environment. All pre-remediation synthetic SERP records have been reclassified to `demo_observation` (`is_demo = 1`) so zero unverified rankings are reported. |
| **5. Multi-Date Visibility Comparison** | **5 Verified Two-Date Pairs** (`2026-10-24` vs `2026-10-25`) | `5` question/provider/market pairs (`Q-001` US/IN, `Q-088` US/IN, `Q-089` US) have verified 2-pass live Gemini observations on both `2026-10-24` and `2026-10-25`. |
| **6. Technical Website Audit (`incubrix.com`)** | **13 Live Pages Crawled**<br>**0 / 22 Live Deployed**<br>**22 / 22 Candidate Patches Validated** | - **Live Crawl**: `13` public URLs + `robots.txt` + `sitemap.xml` crawled from `https://incubrix.com` with raw HTML saved in `data/evidence/crawl/`.<br>- **Live Website Fixes (`validated`)**: **`0 / 22`** (we do not administer `incubrix.com`; all 22 issues remain open on the live domain).<br>- **Candidate Patch Validation (`patch_validated`)**: **`22 / 22`** ready-to-apply code/JSON-LD patches in `data/evidence/patches/` pass issue-specific automated validators (`validate_single_issue_patch`). |
| **7. Content Studio Pages** | **10 Total Pages** (`4` Publish-Ready, `2` Reviewed, `4` Draft) | - **`4` `ready_to_publish`** (`PAGE-004`, `PAGE-005`, `PAGE-008`, `PAGE-010`): Pass all 4 automated checks (content/word count >= 350, verified citations on `DEFAULT_SITEMAP_URLS`, internal links with descriptive anchors >= 10 chars, valid `schema.org` JSON-LD) AND have `0` `unverified_claims_flagged`.<br>- **`2` `reviewed`** (`PAGE-006`, `PAGE-007`) & **`4` `draft`** (`PAGE-001`, `PAGE-002`, `PAGE-003`, `PAGE-009`): Gated from `ready_to_publish` because they contain `unverified_claims_flagged` items (`/signal` analytics roadmap features or unverified third-party pricing dates) requiring human sign-off. |
| **8. Third-Party Citation Opportunities** | **30 Researched URLs** (`17` Verified Live HTTP 200, `11` Pending WAF Check, `2` Unreachable) | Checked via live HTTP requests (`verify_single_citation_url`) with per-URL JSON evidence saved in `data/evidence/citations/CIT-001.json` .. `CIT-030.json`:<br>- **`17` `verified_live`**: Returned `HTTP 200` live (`futurepedia.io`, `buffer.com/bluesky`, `sproutsocial.com`, `later.com`, `creators.spotify.com`, `reddit.com`, `indiehackers.com`, `news.ycombinator.com`, `llmstxt.org`, etc.).<br>- **`11` `pending_check`**: Returned `HTTP 403` Cloudflare/WAF bot protection (`g2.com`, `capterra.com`, `producthunt.com`, `alternativeto.net`, `trustradius.com`, `theresanaiforthat.com`, `getapp.com`).<br>- **`2` `unreachable`**: Returned `HTTP 500` (`buffer.com/resources/content-repurposing-guide/`) or network timeout. |
| **9. Weekly Report & 90-Day Launch Plan** | **1 Weekly Report** + **12-Week Launch Plan** | Generated from verified SQLite metrics into `exports/weekly_visibility_report.md` and `exports/workbook/06_launch_plan_90_days.csv`. |

---

## 3. Incomplete Requirements & Why They Remain Incomplete

1. **Live Automated Collection for OpenAI (`chatgpt`), Perplexity (`perplexity`), Anthropic (`claude`), and Google SERP (`google_search`) (`8` `not_collected` records):**
   - **Why incomplete:** Only `GEMINI_API_KEY` is present in the environment. Paid API keys for `OPENAI_API_KEY`, `PERPLEXITY_API_KEY`, `ANTHROPIC_API_KEY`, and `SERPAPI_API_KEY` / `GOOGLE_CSE_API_KEY` are not configured.
   - **How handled:** The engine records `collection_status = 'not_collected'` honestly (never fabricating responses) and provides a **Manual Evidence Ingestion** workflow (`POST /api/visibility/manual` and UI form) that enforces the same 2-pass disk-evidence verification rule.
2. **Gemini Google Search Grounding Quota on Free Tier (`0.0%` AI Citation Rate on Ungrounded `gemini-3.5-flash-lite`):**
   - **Why incomplete:** Enabling the `{"google_search": {}}` grounding tool on the free-tier `GEMINI_API_KEY` returns `HTTP 429 RESOURCE_EXHAUSTED (limit: 0)`. Standard `gemini-3.5-flash-lite` responds reliably in `~1.8s`–`6s` across `US`, `IN`, and `GB`, but does not attach grounded web citation URLs (`0 / 36` citations).
3. **11 Citation Target URLs Behind Cloudflare / Bot WAF (`HTTP 403`) & 2 Unreachable URLs (`HTTP 500`):**
   - **Why incomplete:** Directories such as G2 (`CIT-001`, `CIT-002`), Capterra (`CIT-003`, `CIT-004`), Product Hunt (`CIT-005`, `CIT-006`), AlternativeTo (`CIT-007`, `CIT-008`), TrustRadius (`CIT-011`, `CIT-012`), and There's An AI For That (`CIT-015`) block automated Python HTTP clients with Cloudflare `HTTP 403`, and `https://buffer.com/resources/content-repurposing-guide/` (`CIT-016`) currently returns `HTTP 500` upstream.
   - **How handled:** Saved exact HTTP status codes in `data/evidence/citations/CIT-XXX.json` and labelled them `pending_check` (`11`) and `unreachable` (`2`) rather than faking `verified_live`.
4. **0 / 22 Technical Fixes Deployed on Live `https://incubrix.com`:**
   - **Why incomplete:** `https://www.incubrix.com` is the external assessment target; we do not have write access to its production codebase or DNS/server configuration.
   - **How handled:** Distinguished `live_site_deployed_fixes = 0` (`validation_status = 'validated'`) from `fixes_validated_patch_tests = 22` (`validation_status = 'patch_validated'`).
5. **6 / 10 Content Studio Pages Gated in `draft` (`4`) or `reviewed` (`2`):**
   - **Why incomplete:** Pages `PAGE-001`, `PAGE-002`, `PAGE-003`, `PAGE-006`, `PAGE-007`, and `PAGE-009` reference either IncuBrix `/signal` analytics features marked *"Coming soon"* on the live site or competitor pricing dates that require human editorial sign-off (`unverified_claims_flagged` is non-empty).

---

## 4. Commands to Run the Application, Engine CLI & Tests

### Initialize / Rebuild Database, Run Live Audit & Export All CSVs
```powershell
# Full initialization with live HTTP crawl of incubrix.com and live HTTP check of 30 citation URLs
python -m engine.cli init --live-audit

# Fast initialization using cached crawl/citation evidence on disk
python -m engine.cli init --no-live-audit
```

### Run the Visibility Collection Engine
```powershell
# Key-free test mode (verifies pipeline without overwriting or promoting pending/failed records)
python -m engine.cli run-visibility --mode test --markets US,IN,GB --limit 10 --pass-number 1

# Live API mode (calls configured providers such as Gemini across US, IN, GB)
python -m engine.cli run-visibility --mode live --markets US,IN,GB --providers gemini --limit 5 --date 2026-10-25 --pass-number 1
python -m engine.cli run-visibility --mode live --markets US,IN,GB --providers gemini --limit 5 --date 2026-10-25 --pass-number 2
```

### Run Individual Engine Commands
```powershell
# Run Technical SEO / AEO / GEO audit against incubrix.com
python -m engine.cli audit

# Generate an AEO/GEO Content Brief for any question ID
python -m engine.cli generate-brief --question-id Q-001 --content-type how_to_guide

# Generate Weekly Visibility Report
python -m engine.cli generate-report

# Export all CSVs (exports/visibility.csv, creator_questions_100.csv, citation_opportunities_30.csv) + 6-tab workbook bundle
python -m engine.cli export-all
```

### Start the Full-Stack Web Application (Express API + React/Vite Dashboard)
```powershell
npm run dev
# Opens at http://localhost:3000
```

### Run All Automated Tests
```powershell
# Run Python unit tests + Vitest API & Zod validation tests
npm test

# Run Playwright end-to-end browser tests
npm run test:e2e
```

---

## 5. Evidence & Export Folder Locations

| Path | Description |
| :--- | :--- |
| [`data/incubrix.db`](../data/incubrix.db) | Local SQLite database storing all questions, observations, crawled pages, technical issues, content pages, citation targets, reports, and launch plan tasks. |
| [`data/evidence/live_gemini_verified.json`](../data/evidence/live_gemini_verified.json) | `37` genuine live `gemini-3.5-flash-lite` API responses (`36` two-pass verified + `1` single-pass pending) across `US`, `IN`, and `GB` on `2026-10-24` and `2026-10-25`. |
| [`data/evidence/observations/`](../data/evidence/observations/) | Individual raw JSON evidence payloads per observation (`OBS-Q-*.json` for non-demo observations; `OBS-DEMO-Q-*.json` for `DEMO` observations). |
| [`data/evidence/crawl/`](../data/evidence/crawl/) | Raw HTML snapshots of all `13` public `incubrix.com` pages + `robots.txt` + `sitemap.xml` + `llms_txt.txt`. |
| [`data/evidence/patches/`](../data/evidence/patches/) | `22` ready-to-apply code and `schema.org` JSON-LD patch files (`ISS-001.patch.txt` .. `ISS-022.patch.txt`). |
| [`data/evidence/citations/`](../data/evidence/citations/) | `30` live HTTP verification evidence files (`CIT-001.json` .. `CIT-030.json`) recording `http_status`, `final_url`, `fetched_title`, and `checked_at`. |
| [`exports/visibility.csv`](../exports/visibility.csv) | Official non-demo visibility observation export (`47` rows) with traceable `raw_evidence_path` references (mirrored at `exports/visibility_observations.csv`). |
| [`exports/creator_questions_100.csv`](../exports/creator_questions_100.csv) | All `100` validated creator questions with source URLs, original wording, and merged duplicate provenance. |
| [`exports/citation_opportunities_30.csv`](../exports/citation_opportunities_30.csv) | All `30` researched third-party citation opportunities with truthful verification status (`17` `verified_live`, `11` `pending_check`, `2` `unreachable`). |
| [`exports/content_pages/`](../exports/content_pages/) | Markdown (`.md`) and standalone JSON-LD (`.schema.json`) files for all `10` Content Studio pages (`PAGE-001` .. `PAGE-010`). |
| [`exports/weekly_visibility_report.md`](../exports/weekly_visibility_report.md) | Generated Weekly AEO / SEO / GEO Visibility & Technical Audit Report. |
| [`exports/workbook/`](../exports/workbook/) | Complete 6-tab CSV assessment workbook bundle (`01_` through `06_`) + `assessment_workbook_bundle.json`. |

---

## 6. Remaining Work Ranked by Assessment Impact

1. **Configure Paid Search & AI Provider Keys (`SERPAPI_API_KEY`, `OPENAI_API_KEY`, `PERPLEXITY_API_KEY`, `ANTHROPIC_API_KEY`) — *Highest Impact***
   - Adding live keys in `.env` and running `python -m engine.cli run-visibility --mode live --markets US,IN,GB --pass-number 1` and `--pass-number 2` will replace the `8` `not_collected` rows with live multi-pass SERP rankings, AI Overviews, and cited responses from ChatGPT, Perplexity, and Claude.
2. **Expand Live 2-Pass Measurement Across All 100 Creator Questions — *High Impact***
   - Currently `8` distinct questions (`37` live Gemini API observations across `US`, `IN`, `GB`) are measured live in `data/evidence/live_gemini_verified.json`. Running batch passes across all `100` questions will provide full category-level Mention/Citation curves.
3. **Human Editorial Verification of the 6 Flagged Content Studio Pages (`PAGE-001`, `PAGE-002`, `PAGE-003`, `PAGE-006`, `PAGE-007`, `PAGE-009`) — *Medium Impact***
   - Once product leadership confirms the release timeline for `/signal` analytics and reviews competitor pricing dates, clearing `unverified_claims_flagged` will promote those 6 pages from `draft`/`reviewed` to `ready_to_publish`.
4. **Browser-Assisted Verification of the 11 Cloudflare-Protected Citation Targets (`CIT-001`..`CIT-012`, `CIT-015`) — *Medium Impact***
   - Capturing authenticated browser snapshots for the 11 `HTTP 403` directory URLs (G2, Capterra, Product Hunt, AlternativeTo, TrustRadius, There's An AI For That) and replacing the broken `HTTP 500` Buffer URL (`CIT-016`) will complete live verification across all 30 citation targets.
5. **Deploy the 22 Candidate Technical Patches to `https://incubrix.com` — *Production Impact***
   - Applying `ISS-001`..`ISS-022` from `data/evidence/patches/` to the live `incubrix.com` Next.js production app and re-running `python -m engine.cli audit` will transition `live_site_deployed_fixes` from `0 / 22` to `22 / 22`.
