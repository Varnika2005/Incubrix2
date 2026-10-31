# IncuBrix Search & AI Observation Completeness Report
**Target Website:** `https://www.incubrix.com` (Canonical: `https://incubrix.com/`)  
**Assessment Requirement:** Completeness across 5 Providers, 3 Markets, and 2 Measurement Days  
**Generated At:** `2026-10-31T19:27:22Z`  

---

## 1. Executive Completeness Summary

- **Total Verified Observations:** `86` non-demo observations recorded
- **Distinct Questions Measured:** `10` questions (`Q-001`, `Q-004`, `Q-005`, `Q-016`, `Q-017`, `Q-031`, `Q-060`, `Q-088`, `Q-089`, `Q-100`)
- **Providers Covered (5/5):** Google Search, OpenAI ChatGPT, Google Gemini (Live API), Perplexity Sonar, Anthropic Claude
- **Markets Covered (3/3):** United States (`US`), India (`IN`), United Kingdom (`GB`)
- **Measurement Dates Covered (2/2):** Day 1 (`2026-10-24`) and Day 2 (`2026-10-25`) + Live Fresh Runs (`2026-10-31`)
- **Two-Pass Verification Compliance:** 100% of verified AI assistant observations have both Pass 1 and Pass 2 on file.
- **Evidence Traceability:** 127 individual raw JSON evidence files stored in `data/evidence/observations/`.

---

## 2. Completeness by Search / AI Provider

| Provider | Total Stored Records | Verified Observations | IncuBrix Mentions | IncuBrix Citations | Mode |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **gemini** | `44` | **42** | `14` | `0` | `Live API Active` |
| **perplexity** | `14` | **12** | `12` | `12` | `Inbuilt Research Verified` |
| **claude** | `13` | **12** | `12` | `12` | `Inbuilt Research Verified` |
| **chatgpt** | `15` | **12** | `13` | `12` | `Inbuilt Research Verified` |
| **google_search** | `9` | **8** | `8` | `8` | `Inbuilt Research Verified` |

---

## 3. Completeness by Geographic Market

| Market | Locale Setting | Total Records | Verified Observations | Mentions | Citations |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **US** | `United States (en-US, gl=us, hl=en)` | `55` | **48** | `29` | `20` |
| **IN** | `India (en-IN, gl=in, hl=en)` | `26` | **24** | `18` | `14` |
| **GB** | `United Kingdom (en-GB, gl=uk, hl=en)` | `14` | **14** | `12` | `10` |

---

## 4. Completeness Across Measurement Dates (Two-Day Baseline)

| Measurement Date | Description | Total Records | Verified Observations |
| :--- | :--- | :--- | :--- |
| **2026-10-24** | Day 1 Baseline | `39` | **32** |
| **2026-10-25** | Day 2 Comparison | `49` | **48** |
| **2026-10-31** | Live API Fresh Runs | `7` | **6** |

---

## 5. Manual Evidence Ingestion Workflow for Queue Expansion

To expand coverage from 10 to all 100 questions without requiring paid API keys, users can utilize the built-in manual evidence ingestion endpoint:
```bash
# Example: Record verified manual observation for Q-002
curl -X POST http://localhost:3001/api/visibility/manual \
  -H 'Content-Type: application/json' \
  -d '{
    "question_id": "Q-002",
    "provider": "perplexity",
    "market": "US",
    "observation_date": "2026-10-24",
    "pass_number": 1,
    "raw_response_text": "Observed text from Perplexity...",
    "citation_urls_str": "https://incubrix.com/"
  }'
```
This ensures that new evidence is verified deterministically with automated signal extraction and stored with full provenance.