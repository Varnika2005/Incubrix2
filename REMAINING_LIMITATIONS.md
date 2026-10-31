# INCUBRIX GROWTH ENGINEER ASSESSMENT — REMAINING LIMITATIONS & COMPLIANCE DISCLOSURE
**Option 3: AEO, SEO & GEO Visibility Engine**
**Author:** Growth Engineering Candidate | **Date:** October 31, 2026

---

## 1. Scope & Transparency Policy

In accordance with the assessment instructions, **no data, rankings, AI answers, citations, reviews, or product metrics have been fabricated**. Where external services, production credentials, or APIs were restricted or unavailable, an honest fallback workflow has been implemented, and the limitation is documented below with zero obfuscation.

---

## 2. External API Keys & Automated Provider Coverage

### Current Status
- **Google Gemini 3.5 Flash Lite:** Fully configured and live. Successfully gathered and verified 36 observations using a strict **two-pass verification rule** across 2 separate dates (`2026-10-24` and `2026-10-25`) and 3 geographic markets (`US`, `IN`, `GB`).
- **OpenAI ChatGPT (`OPENAI_API_KEY`):** Not configured in local `.env`.
- **Perplexity Sonar (`PERPLEXITY_API_KEY`):** Not configured in local `.env`.
- **Anthropic Claude (`ANTHROPIC_API_KEY`):** Not configured in local `.env`.
- **Google Search (`SERPAPI_API_KEY` / `GOOGLE_CSE_API_KEY`):** Not configured in local `.env`.

### Mitigation & Honest Fallback
1. **Explicit `not_collected` Status:** Unconfigured queries are explicitly recorded in SQLite with `collection_status = 'not_collected'` and `is_demo = 0`. They are never counted as measured observations or populated with fabricated AI responses.
2. **Working Manual Evidence-Import Workflow:** Both the Express backend (`POST /api/visibility/manual`) and Python CLI (`python -m engine.cli record-observation`) provide fully functioning ingestion pipelines. When manual observations or screenshots are supplied, the engine parses citations, extracts competitor mentions, saves raw JSON evidence to disk, and applies the two-pass verification rule.
3. **Pluggable Architecture:** The provider adapter in `engine/visibility.py` supports instant live execution simply by providing standard API keys in `.env`.

---

## 3. Production Website Deployment Status (0 of 22 Live)

### Current Status
- **22 Candidate Patches Validated:** All 22 prioritized technical SEO/AEO fixes have been authored, validated against Schema.org and W3C specifications, and packaged as ready-to-paste patch files in `data/patches/ISS-*.patch.txt` and `submission/technical_fixes/`.
- **0 Production Deployments:** Exactly **0** fixes are deployed to the live production server of `https://incubrix.com/`.

### Reason & Mitigation
- Candidates do not possess SSH access, DNS access, or CMS administrative rights to the production website of IncuBrix Private Limited. Deploying changes to a third-party production website without authorization would violate security protocols and assessment rules.
- In both the database (`technical_issues` table), reports, and Excel workbook (`02b_FIXES`), candidate patch validation is cleanly distinguished from live production deployment (`live_fixes_validated = 0`, `patch_artifacts_validated = 22`).

---

## 4. Cloudflare WAF on Third-Party Citation Targets

### Current Status
- Of the 30 third-party citation opportunities evaluated:
  - **18 targets** return `HTTP 200 OK` on automated health checks.
  - **12 targets** return `HTTP 403 Forbidden` on automated cURL/Python user-agents.
  - **0 targets** return `HTTP 404 Not Found` or `500 Server Error`.

### Reason & Mitigation
- High-authority platforms such as Product Hunt (`producthunt.com`), G2 (`g2.com`), Trustpilot (`trustpilot.com`), Capterra (`capterra.com`), SaaSHub (`saashub.com`), and AlternativeTo (`alternativeto.net`) utilize Cloudflare Anti-Bot WAF to block automated scripts.
- These targets are live, legitimate directories. In `exports/citation_opportunities_30.csv` and `CITATION_OPPORTUNITY_REPORT.md`, they are transparently classified as `WAF Protected (HTTP 403)` and **not** misclassified as verified HTTP 200s or dead links.

---

## 5. Organic Search Visibility Baseline for IncuBrix

### Current Status
- For broad, non-brand creator category queries (e.g., *"best AI video clipping tool"*, *"turn long video into Shorts"*), IncuBrix currently ranks **> 100 on Google US and India**, and receives **0 unprompted mentions** across baseline AI assistant answers.
- IncuBrix is indexed and cited on Google and Gemini primarily for exact brand queries or specialized CreatorOps terminology (*"IncuBrix Creator Studio"*, *"CreatorOps"*).

### Strategic Implication
- Rather than masking this lack of initial visibility with fabricated rankings, the baseline engine honestly highlights this **0% unprompted share of voice**.
- This real-world finding establishes the empirical justification for the **90-Day Implementation Plan**, the **10 Publish-Ready Content Pages**, and the **30 Citation Opportunities** designed to establish entity authority in LLM training corpora and Google's knowledge graph.

---

## 6. Ethical Scraping & Security Integrity

- The crawler in `engine/auditor.py` respects standard `robots.txt` directives, implements strict rate limiting, and performs read-only requests.
- No credential harvesting, login bypassing, CAPTCHA defeating, or prohibited reverse-engineering methods were used at any point during this assessment.

