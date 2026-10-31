# IncuBrix Weekly AEO / SEO / GEO Visibility Report
**Report ID:** `REP-WEEKLY-20261031`  
**Target Property:** `https://www.incubrix.com` (Canonical: `https://incubrix.com/`)  
**Reporting Period:** `2026-10-20` to `2026-10-24`  
**Generated At:** `2026-10-31T19:53:43Z`

---

## 1. Coverage & Data-Quality Summary (DEMO Records Excluded)

| Metric | Measured Value | Notes |
| :--- | :--- | :--- |
| **Creator Questions Validated** | **100 / 100** | 6 duplicate source variants merged preserving full provenance |
| **Questions Measured (Non-Demo)** | **8** | Measured across US (`en-US`), India (`en-IN`), and UK (`en-GB`) |
| **Verified Observations (>=2 Passes / SERP)** | **36** | Raw JSON evidence stored in `data/evidence/observations/` |
| **Pending Verification (Single AI Pass)** | **1** | Requires Pass 2 check before counting as verified |
| **Not Collected (No Paid API Key)** | **7** | Awaiting live provider credentials or manual evidence |
| **Failed Collection (Timeouts / 429s)** | **2** | Logged transparently with error trace |
| **Demonstration Data (`DEMO` Excluded)** | **34** | Explicitly labelled `DEMO` and excluded from all totals |

---

## 2. Search & AI Visibility Observations

- **Google Search Observations:** `0` verified SERP checks (`0` with top-10 IncuBrix organic rank on brand/CreatorOps queries; `0` Answer Box observations; `0` AI Overviews observed, `0` citing `incubrix.com`).
- **AI Assistant Mention Rate (Measured Sample):** **38.9%** (`14` / `36` non-demo AI observations).
- **AI Assistant Citation Rate (Measured Sample):** **0.0%** (`0` / `36` non-demo AI observations).
- **Key Insight:** IncuBrix achieves strong visibility on `CreatorOps`, credit-validity, 5-platform publishing (including Bluesky & Spotify), and direct brand comparison queries (`Q-001`, `Q-005`, `Q-060`, `Q-088`, `Q-089`), but has **0% unprompted visibility** on generic non-branded category queries (`Q-016` transcript video editing, `Q-017` 1-hour-to-12-clips) where Descript and OpusClip dominate.

### Multi-Date Visibility Comparison (`2026-10-24` vs `2026-10-25`)
Paired two-day verified observations: **5** pairs (`+0` gained citations, `0` Google rank improvements).

| Question ID | Provider & Market | Mention (`2026-10-24` -> `2026-10-25`) | Citation (`2026-10-24` -> `2026-10-25`) | Google Rank (`2026-10-24` -> `2026-10-25`) |
| :--- | :--- | :--- | :--- | :--- |
| `Q-001` | gemini (IN) | No -> No | No -> No | - -> - |
| `Q-001` | gemini (US) | No -> No | No -> No | - -> - |
| `Q-088` | gemini (IN) | Yes -> Yes | No -> No | - -> - |
| `Q-088` | gemini (US) | Yes -> Yes | No -> No | - -> - |
| `Q-089` | gemini (US) | Yes -> Yes | No -> No | - -> - |

---

## 3. Competitor Share of Voice in Observed Responses

| Competitor | Observed Mentions (Non-Demo) |
| :--- | :--- |
| Munch | 13 |
| OpusClip | 12 |
| Descript | 8 |
| Castmagic | 6 |
| Repurpose.io | 2 |
| Kapwing | 2 |
| Buffer | 2 |
| Hootsuite | 2 |

---

## 4. Technical SEO / AEO / GEO Audit & Validation Progress

- **Live Pages Crawled on `incubrix.com`:** `0` sitemap URLs + `robots.txt` + `sitemap.xml` + `/llms.txt` check.
- **Total Prioritized Findings:** **22** (`3` Critical, `4` High, `10` Medium, `5` Low).
- **Live Website Fixes Deployed (`incubrix.com`):** **0 / 22** (we do not administer the live `incubrix.com` server; all 22 issues remain open on the live site).
- **Candidate Patch Validation Status:** **22 / 22** ready-to-apply code/JSON-LD patches passed automated issue-specific validation (`validate_single_issue_patch`).

---

## 5. Content Studio & Third-Party Citation Pipeline

- **Content Studio Pages Completed:** **10** pages (`10` Ready to Publish, `0` Reviewed, `0` Draft). Pages with unverified feature claims (`/signal` analytics, automated optimal-time scheduling) are gated in `draft` or `reviewed` until human verification.
- **Citation Opportunities Researched:** **30** specific third-party URLs across G2, Capterra, Product Hunt, AlternativeTo, Futurepedia, There's An AI For That, Buffer, Sprout Social, Spotify for Creators, Reddit, Indie Hackers, and Hacker News (`18` verified HTTP 200 live, `12` HTTP 403 WAF-protected pending manual check, `0` HTTP 500 unreachable).

---

## 6. Failures, Missing Data & Limitations

1. **Unconfigured Paid API Keys (`7` records):** Automated live calls to OpenAI, Gemini, Perplexity, Claude, and SerpApi require API keys in `.env`. Without keys, the engine records `not_collected` honestly and supports manual evidence ingestion.
2. **Failed Requests (`2` records):** Rate-limit (`HTTP 429`) and timeout errors are preserved in `visibility_observations` with exact error messages and never counted as verified observations.
3. **Single-Pass Pending Records (`1` records):** Kept in `pending_verification` until a second independent pass (`pass_number >= 2`) is recorded.

---

## 7. Prioritized Next Actions (Week 1–2 Execution)

1. **Deploy `ISS-001` through `ISS-004` & `ISS-007` JSON-LD Schemas + `ISS-002` `/llms.txt`** to `https://incubrix.com/` to establish machine-readable entity authority.
2. **Fix `ISS-005` & `ISS-006` on `/manifesto`** (populate the empty `<h1>` tag and add global header/footer internal navigation links).
3. **Publish the 10 Content Studio Guides** under `https://incubrix.com/guides/*` to capture comparative (`IncuBrix vs OpusClip vs Descript`) and how-to (`1-Hour Video to 12 Clips`) queries.
4. **Submit Tier-1 Software Directory Listings (`CIT-001` to `CIT-015`)** on G2, Capterra, Product Hunt, AlternativeTo, and Futurepedia.
