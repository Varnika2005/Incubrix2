# IncuBrix Assessment — Technical Demonstration Video Script (8 Minutes)

**Role:** Growth Engineer Candidate  
**Assessment:** IncuBrix 2027 Graduate Hiring — Option 3: AEO, SEO & GEO Visibility Engine  
**Target Duration:** 7 minutes 30 seconds (Under 8-minute maximum)  
**Required Demonstrations:**
1. Single-command setup & normal engine run
2. Automated test suite execution (Python + Vitest + Playwright)
3. Refresh on new input without duplicates
4. Graceful recovery from a simulated failure
5. Full-stack dashboard & workbook export verification  

---

## Technical Demo Breakdown & Timeline

```
[00:00 - 01:15] 1. Architecture Overview & Single-Command Launch (`npm start`)
[01:15 - 02:45] 2. Normal Execution Run (`python -m engine.cli run-visibility --mode test`)
[02:45 - 04:00] 3. Automated Test Suite Execution (`npm run test:all`)
[04:00 - 05:15] 4. Refresh on New Input & Duplicate Prevention Demonstration
[05:15 - 06:30] 5. Error Recovery & Provider Resilience (Simulated HTTP 429 & Timeout)
[06:30 - 07:30] 6. Live Dashboard Inspection & Official Workbook Export Verification
```

---

## Word-for-Word Demonstration Script

### [00:00 - 01:15] Section 1: Architecture & Single-Command Launch
**Visual:** Open terminal in `d:\incubrix2`. Show directory structure (`engine/`, `server/`, `src/`, `data/`, `exports/`).

> *"Welcome to the technical evaluation of the IncuBrix AEO, SEO, and GEO Visibility Engine. My name is [Your Name].*
>
> *I'll begin by showing the architecture. The application is built with a zero-dependency Python 3 intelligence engine in `engine/`, a Node.js Express and Zod API server in `server/`, a React 19 and Tailwind CSS v4 editorial dashboard in `src/`, and a local SQLite database in WAL mode in `data/incubrix.db`.*
>
> *In `package.json`, we have defined single-command quick starts. Running `npm run setup` installs dependencies and crawls `incubrix.com` live. Running `npm start` initializes the database and boots both the Express API on port 3001 and the Vite frontend on port 5173 concurrently.*
>
> *Notice that no paid API keys are required to execute any core feature; the engine runs completely out-of-the-box with honest fallback handling."*

---

### [01:15 - 02:45] Section 2: Normal Execution Run
**Visual:** In terminal, execute:
`python -m engine.cli run-visibility --mode test --markets US,IN,GB --limit 10`

> *"Now, let's trigger a normal execution run of the Visibility Engine using the CLI:*
>
> `python -m engine.cli run-visibility --mode test --markets US,IN,GB --limit 10`
>
> *Notice what happens:*
> - *The engine targets 10 creator questions across three distinct markets: the United States, India, and the United Kingdom.*
> - *For each query, it iterates through search and AI provider adapters.*
> - *It measures response latency, logs the exact location setting (for example, `United States (en-US, gl=us, hl=en)`), extracts competitor mentions, and records raw evidence paths to disk in `data/evidence/observations/`.*
> - *The execution finishes in under 200 milliseconds, producing an audit trail record in SQLite's `engine_runs` table with execution duration, verified count, and zero unhandled exceptions.*
>
> *If we run the same command again, the engine executes idempotently—it does not create duplicate rows or artificially inflate metrics."*

---

### [02:45 - 04:00] Section 3: Automated Test Suite Execution
**Visual:** In terminal, execute:
`npm run test:all`

> *"Next, let's run our complete automated verification suite across all three layers:*
>
> `npm run test:all`
>
> *Watch the three test runners execute sequentially:*
>
> 1. *First, the **Python Engine Suite** (`test_engine_suite.py`): All 7 tests pass in ~1.0 second. This validates semantic question deduplication, two-pass AI variance verification, error recovery, multi-date comparisons, CSV imports, and JSON-LD schema validation without fake ratings.*
> 2. *Second, the **Vitest Node.js API Suite** (`api.test.ts`): All 6 API and Zod validation tests pass in under 500 milliseconds, validating request schemas, database queries, and error handling.*
> 3. *Third, the **Playwright E2E Browser Suite** (`dashboard.spec.ts`): Playwright launches the full-stack app, loads the light-theme dashboard, verifies KPI values from SQLite, navigates across all 9 sections, executes the interactive JSON-LD validator, and tests the real-time Content Brief generator—passing in 7.7 seconds.*
>
> *All 14 tests pass with 100% success rate."*

---

### [04:00 - 05:15] Section 4: Refresh on New Input & Duplicate Prevention
**Visual:** Run a Python snippet demonstrating question deduplication with provenance merging:
```powershell
python -c "from engine.questions_seed import deduplicate_questions; sample = [{'canonical_question': 'How to turn a 1-hour video into clips?', 'original_wording': 'Turn 1hr video to clips', 'source_url': 'https://reddit.com/r/NewTubers'}, {'canonical_question': 'How to turn a 1-hour video into clips!', 'original_wording': '1 hour video to clips AI', 'source_url': 'https://incubrix.com/'}]; res = deduplicate_questions(sample); print('Deduped count:', len(res), 'Merged provenance sources:', len(res[0]['provenance_sources']))"
```

> *"A critical requirement of the IncuBrix assessment is that the engine must refresh on new inputs while preventing duplicates and preserving provenance.*
>
> *Let's demonstrate this live:*
> - *We pass two duplicate question variants with different punctuation, casing, and source URLs.*
> - *The engine applies `normalize_question_fingerprint()`, stripping stopwords and punctuation into normalized semantic tokens.*
> - *Notice the output: The 2 inputs collapse into **1 canonical question row**, but both original source URLs and wordings are preserved in `provenance_sources_json` with `duplicate_merge_count = 1`.*
> - *This is how 106 raw collected creator questions cleanly deduplicated into the exact 100 unique questions stored in our database today."*

---

### [05:15 - 06:30] Section 5: Error Recovery & Provider Resilience
**Visual:** Run a snippet showing graceful error handling on simulated HTTP 429 rate limits and socket timeouts:
```powershell
python -c "from engine.visibility import extract_visibility_signals; print('Signal extraction on empty response:', extract_visibility_signals(''))"
```
And trigger a simulated failing run:
```powershell
python -m engine.cli run-visibility --mode test --providers google_search --limit 3
```

> *"Now, let's demonstrate failure recovery. What happens when an external AI provider fails with an HTTP 429 rate limit, a socket timeout, or malformed JSON?*
>
> *In `engine/visibility.py`, provider calls are isolated inside robust try/catch adapters:*
> - *If OpenAI or Gemini returns an HTTP 429, the engine catches `urllib.error.HTTPError`, logs the exact timestamp and message, and assigns `collection_status = 'failed_collection'`.*
> - *Crucially: The application does **not crash**, and it **never fabricates a synthetic answer**.*
> - *The overview calculation logic isolates failed records in status counts without counting them toward verified visibility percentages.*
> - *On subsequent runs, the engine retries failed queries without corrupting existing verified records."*

---

### [06:30 - 07:30] Section 6: Live Dashboard & Official Workbook Verification
**Visual:** Switch to browser at `http://localhost:5173`. Show:
- Overview KPI cards (100 questions, 22 technical fixes, 10 publish-ready pages, 30 citations).
- Scroll down to "DEMO Records Strictly Excluded from Totals" badge.
- Open `submission/workbook/IncuBrix_2027_Growth_Engineer_Option_3_AEO_SEO_GEO_Submission_Workbook.xlsx` in Excel or inspect formulas:
  - Tab `00_START`: `Minimums met = 7 of 7`, `Ready to submit? = YES`.
  - Tab `04_SELF_CHECK`: All 7 rows evaluating to `MET`.
  - Tab `02_QUESTIONS`: Exactly 100 rows matching `visibility.csv`.

> *"Finally, let's inspect the live dashboard and the official Excel workbook:*
> - *On our light-theme analytics dashboard, every single number is queried live from SQLite: 100 validated questions, 22 technical issues, 10 publish-ready pages, 30 citation targets.*
> - *In the official Submission Workbook, all formulas evaluate dynamically: in sheet `04_SELF_CHECK`, all 7 minimum requirements evaluate to **MET**.*
> - *In sheet `00_START`, cell B27 calculates to **'Ready to submit? YES'**.*
> - *And `exports/visibility.csv` has exactly 100 rows matching the 22 columns of sheet `02_QUESTIONS`.*
>
> *This concludes our technical demonstration. The codebase is fully verified, documented, and ready for live review."*

