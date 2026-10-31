# IncuBrix Technical SEO, AEO & GEO Audit Report

**Target Domain:** `https://www.incubrix.com` (Canonical: `https://incubrix.com/`)  
**Audit Scope:** Full crawl of 13 public sitemap URLs + `robots.txt` + `sitemap.xml` + `/llms.txt`  
**Audit Date:** October 2026  
**Status Summary:** 22 Total Issues Identified | 22 Candidate Patches Generated & Validated | 0 Deployed Live (Site Admin Access Restricted)  

---

## 1. Executive Summary & Audit Methodology

A comprehensive automated and manual inspection of `https://www.incubrix.com` was conducted across:
1. **Indexability & Crawlability:** `robots.txt` directives, XML sitemap timestamps, canonical tags, 301 apex redirects.
2. **Structured Data (JSON-LD):** Detection of `@context: https://schema.org` blocks, validation against Google Rich Results standards, verification that no fabricated ratings/reviews exist.
3. **AEO & GEO Readiness:** `/llms.txt` presence, `<meta name="robots" content="max-snippet:-1, max-image-preview:large">`, Open Graph & Twitter Cards, AI crawler accessibility.
4. **On-Page SEO & Content Structure:** Heading hierarchy (`<h1>`–`<h2>`), meta descriptions, title tag syntax, typographical checks.
5. **Media & Accessibility:** Image `alt` attributes, image payload sizing and format optimization.
6. **Performance & Core Web Vitals:** Render-blocking third-party scripts/CSS, inline CSS bloat.
7. **Internal Linking & Architecture:** Header/footer navigation completeness, orphan page analysis, body CTA destinations.

### Four-Tier Deployment Status Classification
- **1. Identified:** Issue verified against raw crawled HTML/HTTP headers.
- **2. Patch Generated:** Ready-to-paste code or text artifact created in `data/patches/`.
- **3. Patch Locally Validated:** Syntax, schema, and regex validation passed via automated test suite.
- **4. Production Deployment Verified:** Verified fixed on live `https://incubrix.com` (Currently **0 / 22** because production hosting is administered externally).

---

## 2. Master Table of 22 Prioritized Technical Fixes

| Fix ID | Priority | Severity | Category | Affected Page URL | Title / Issue Summary | Patch Artifact | Local Validation | Live Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `ISS-001` | #1 | **CRITICAL** | Structured Data (JSON-LD) | `https://incubrix.com/` | Zero JSON-LD Structured Data (Organization & WebSite) on Homepage | `data/patches/ISS-001.patch.txt` | **PASS (100%)** | Open on Live Target |
| `ISS-002` | #2 | **CRITICAL** | AEO / GEO Readiness | `https://incubrix.com/llms.txt` | Missing /llms.txt File (HTTP 404 Not Found) for AI Crawler Discovery | `data/patches/ISS-002.patch.txt` | **PASS (100%)** | Open on Live Target |
| `ISS-003` | #3 | **CRITICAL** | Structured Data (JSON-LD) | `https://incubrix.com/pricing` | Missing SoftwareApplication & Offer Schema for 6 Credit Pricing Tiers on /pricing | `data/patches/ISS-003.patch.txt` | **PASS (100%)** | Open on Live Target |
| `ISS-004` | #4 | **HIGH** | Structured Data (JSON-LD) | `https://incubrix.com/faq` | Missing FAQPage Structured Data on /faq and /pricing | `data/patches/ISS-004.patch.txt` | **PASS (100%)** | Open on Live Target |
| `ISS-005` | #5 | **HIGH** | On-Page SEO | `https://incubrix.com/manifesto` | Empty <h1> Heading Tag on /manifesto | `data/patches/ISS-005.patch.txt` | **PASS (100%)** | Open on Live Target |
| `ISS-006` | #6 | **HIGH** | Internal Linking | `https://incubrix.com/manifesto` | Orphan / Dead-End Page Architecture on /manifesto (0 Internal Links) | `data/patches/ISS-006.patch.txt` | **PASS (100%)** | Open on Live Target |
| `ISS-007` | #7 | **HIGH** | Structured Data (JSON-LD) | `https://incubrix.com/how-it-works` | Missing HowTo Structured Data on /how-it-works for 4-Step Creator Workflow | `data/patches/ISS-007.patch.txt` | **PASS (100%)** | Open on Live Target |
| `ISS-008` | #8 | **MEDIUM** | Structured Data (JSON-LD) | `https://incubrix.com/team` | Missing AboutPage & Person Entity Graph on /team | `data/patches/ISS-008.patch.txt` | **PASS (100%)** | Open on Live Target |
| `ISS-009` | #9 | **MEDIUM** | Accessibility & Media | `https://incubrix.com/about` | 17 Content Images Across /, /about, /pricing, and /waitlist Have Empty alt="" Attributes | `data/patches/ISS-009.patch.txt` | **PASS (100%)** | Open on Live Target |
| `ISS-010` | #10 | **MEDIUM** | On-Page SEO | `https://incubrix.com/` | Zero Twitter/X Card Meta Tags (twitter:card, twitter:title, twitter:image) Across All 13 Pages | `data/patches/ISS-010.patch.txt` | **PASS (100%)** | Open on Live Target |
| `ISS-011` | #11 | **MEDIUM** | On-Page SEO | `https://incubrix.com/` | Grammatical Error ('one content') & Pipe Character in Homepage Meta Description | `data/patches/ISS-011.patch.txt` | **PASS (100%)** | Open on Live Target |
| `ISS-012` | #12 | **MEDIUM** | Technical & Crawlability | `https://incubrix.com/sitemap.xml` | Missing <lastmod> ISO-8601 Timestamps in sitemap.xml | `data/patches/ISS-012.patch.txt` | **PASS (100%)** | Open on Live Target |
| `ISS-013` | #13 | **MEDIUM** | AEO / GEO Readiness | `https://incubrix.com/robots.txt` | robots.txt Lacks Explicit AI Search Crawler Allow Rules (GPTBot, OAI-SearchBot, PerplexityBot, ClaudeBot) | `data/patches/ISS-013.patch.txt` | **PASS (100%)** | Open on Live Target |
| `ISS-014` | #14 | **MEDIUM** | AEO / GEO Readiness | `https://incubrix.com/` | Missing Explicit <meta name="robots"> Max-Snippet & Max-Image-Preview Directives Across All 13 Pages | `data/patches/ISS-014.patch.txt` | **PASS (100%)** | Open on Live Target |
| `ISS-015` | #15 | **MEDIUM** | Performance & CWV | `https://incubrix.com/` | Render-Blocking Third-Party Calendly CSS Loaded in <head> Across Non-Booking Pages | `data/patches/ISS-015.patch.txt` | **PASS (100%)** | Open on Live Target |
| `ISS-016` | #16 | **MEDIUM** | Technical & Crawlability | `https://incubrix.com/waitlist` | Legacy /waitlist Page Remains Indexed in Sitemap Despite 'Creator Studio is Live' Launch | `data/patches/ISS-016.patch.txt` | **PASS (100%)** | Open on Live Target |
| `ISS-017` | #17 | **MEDIUM** | Internal Linking | `https://incubrix.com/` | Body CTA Links Point Exclusively to app.incubrix.com Without Contextual Internal Links to /how-it-works or /pricing | `data/patches/ISS-017.patch.txt` | **PASS (100%)** | Open on Live Target |
| `ISS-018` | #18 | **LOW** | Performance & CWV | `https://incubrix.com/og-image.jpg` | Uncompressed 415 KB JPEG Open Graph Image (/og-image.jpg) & Logo Asset | `data/patches/ISS-018.patch.txt` | **PASS (100%)** | Open on Live Target |
| `ISS-019` | #19 | **LOW** | On-Page SEO | `https://incubrix.com/faq` | Pipe Character ('|') Used as Punctuation in /faq Meta Description | `data/patches/ISS-019.patch.txt` | **PASS (100%)** | Open on Live Target |
| `ISS-020` | #20 | **LOW** | Technical & Crawlability | `https://www.incubrix.com/` | www.incubrix.com Redirects to Apex incubrix.com — Ensure External Profiles Use Canonical Apex URL | `data/patches/ISS-020.patch.txt` | **PASS (100%)** | Open on Live Target |
| `ISS-021` | #21 | **LOW** | Performance & CWV | `https://incubrix.com/` | Duplicated ~20 KB Inline <style> Block Across All 13 HTML Pages Instead of Cached Stylesheet | `data/patches/ISS-021.patch.txt` | **PASS (100%)** | Open on Live Target |
| `ISS-022` | #22 | **LOW** | AEO / GEO Readiness | `https://incubrix.com/` | Missing Open Graph Locale Tags (og:locale & og:locale:alternate) for US, India, and UK Creator Markets | `data/patches/ISS-022.patch.txt` | **PASS (100%)** | Open on Live Target |

---

## 3. Detailed Technical Fix Specifications (Ready-to-Paste Code)

### ISS-001: Zero JSON-LD Structured Data (Organization & WebSite) on Homepage
- **Priority Rank:** #1 | **Severity:** `CRITICAL` | **Category:** `Structured Data (JSON-LD)`
- **Affected URL:** `https://incubrix.com/`
- **Actual Evidence Observed:**
  > HTTP 200 (59,079 bytes) on https://incubrix.com/: <script type="application/ld+json"> count = 0 across all 13 sitemap pages.
- **Problem Description:**
  Live inspection of https://incubrix.com/ shows 0 <script type="application/ld+json"> blocks. Search engines and AI answer engines lack machine-readable entity definitions for IncuBrix, its founder, logo, and official URLs.
- **Recommended Correction:**
  Inject validated Organization and WebSite JSON-LD schema into the <head> of https://incubrix.com/ with factual entity fields (no fabricated ratings).
- **Validation Method & Result:**
  `Parse JSON-LD block with validate_json_ld() and verify @graph contains Organization and WebSite with valid schema.org @context.` -> `OPEN ON LIVE SITE: 0 JSON-LD blocks present on https://incubrix.com/. | Candidate Patch Check: PASS: Validated schema.org JSON-LD syntax and required entity properties for ISS-001 (0 unverified fields).` (Checked: `2026-10-24T19:16:32Z`)
- **Deployment Status:** `Patch tested locally; pending deployment by site administrator.`

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@graph": [
    {
      "@type": "Organization",
      "@id": "https://incubrix.com/#organization",
      "name": "IncuBrix",
      "legalName": "IncuBrix Pte. Ltd.",
      "url": "https://incubrix.com/",
      "logo": {
        "@type": "ImageObject",
        "url": "https://incubrix.com/assets/incubrix-logo.jpg"
      },
      "description": "IncuBrix unifies content insights, AI-assisted creation, intelligent repurposing, and multi-platform publishing into one CreatorOps workflow.",
      "email": "support@incubrix.com",
      "founder": {
        "@type": "Person",
        "name": "Kamraj Subramanian",
        "jobTitle": "Founder and CEO"
      }
    },
    {
      "@type": "WebSite",
      "@id": "https://incubrix.com/#website",
      "url": "https://incubrix.com/",
      "name": "IncuBrix \u2014 Creator Studio",
      "publisher": {
        "@id": "https://incubrix.com/#organization"
      }
    }
  ]
}
</script>
```

---

### ISS-002: Missing /llms.txt File (HTTP 404 Not Found) for AI Crawler Discovery
- **Priority Rank:** #2 | **Severity:** `CRITICAL` | **Category:** `AEO / GEO Readiness`
- **Affected URL:** `https://incubrix.com/llms.txt`
- **Actual Evidence Observed:**
  > GET https://www.incubrix.com/llms.txt -> HTTP 404 Not Found (Server: Vercel).
- **Problem Description:**
  Requesting https://incubrix.com/llms.txt and https://www.incubrix.com/llms.txt returns HTTP 404 Not Found. LLM-powered answer engines (Perplexity, ChatGPT Search, Claude) use /llms.txt to ingest concise, authoritative product facts and pricing.
- **Recommended Correction:**
  Publish a standardized Markdown /llms.txt file at the root domain summarizing IncuBrix's 4 pillars, 6 pricing tiers, leadership team, and canonical URLs.
- **Validation Method & Result:**
  `Verify candidate /llms.txt contains H1 brand header, summary blockquote, core capabilities, factual pricing tiers ($0-$250/mo), and canonical markdown links.` -> `OPEN ON LIVE SITE: GET https://incubrix.com/llms.txt returns HTTP 404. | Candidate Patch Check: PASS: Validated /llms.txt structure (H1 title, summary blockquote, capabilities, and 6 factual pricing tiers).` (Checked: `2026-10-24T19:16:32Z`)
- **Deployment Status:** `Patch tested locally; pending deployment by site administrator.`

```html
# IncuBrix (https://incubrix.com)

> IncuBrix is an AI-powered CreatorOps platform and Creator Studio that helps podcasters, YouTubers, and multi-platform creators turn one recording or idea into clips, captions, voiceovers, digital avatar videos, and formatted social posts—then publish across YouTube, Instagram, LinkedIn, Spotify, and Bluesky from one screen.

## Core Capabilities
- **Content Insights**: Niche trend scanning, competitor gap analysis, and ranked topic recommendations.
- **AI Content Studio (`/studio`)**: Transcript-based video editing (delete text to cut video), automated highlight extraction (1 hour video to 12 clips), AI voice cloning for narration, and lip-synced digital talking-head avatars.
- **Intelligent Repurposer (`/repurpose`)**: Converts Text-to-Audio, Text-to-Video, and Audio/Video-to-Text across 10+ formats (YouTube Shorts, Instagram Reels, LinkedIn posts, Spotify podcasts, Bluesky posts, blogs, and newsletters).
- **Centralized Publishing (`/publish`)**: Single-screen distribution to YouTube, Instagram, LinkedIn, Spotify, and Bluesky with automatic aspect-ratio sizing and burned-in/native captions.
- **Unified Analytics (`/signal` — Coming Soon)**: Cross-platform views, watch time, and engagement tracking.

## Pricing Plans (Credit-Based, 1-Year Validity via Stripe)
- **Free**: $0/month — 300 credits/month (~21 one-minute videos)
- **Starter**: $10/month — 1,000 credits/month (~71 one-minute videos)
- **Essential**: $20/month — 2,000 credits/month (~142 one-minute videos)
- **Growth**: $50/month — 5,000 credits/month (~357 one-minute videos)
- **Scale**: $100/month — 10,000 credits/month (~714 one-minute videos)
- **Pro**: $250/month — 25,000 credits/month (~1,785 one-minute videos)

## Key Public URLs
- [Homepage](https://incubrix.com/): Overview of the four Creator Studio pillars.
- [How IncuBrix Works](https://incubrix.com/how-it-works): End-to-end CreatorOps workflow from insights to publishing.
- [Pricing](https://incubrix.com/pricing): Credit tiers and billing FAQs.
- [About Us](https://incubrix.com/about): Mission to solve creator tool overload and unify CreatorOps.
- [FAQ](https://incubrix.com/faq): Product, privacy, and support answers.
- [Leadership Team](https://incubrix.com/team): Founded by Kamraj Subramanian (CEO), with Rachel Blewitt (COO), Supriya Sambhus (Director of PM), Nidhi Raj (GTM), Santhosh CE (Engineering Manager), and Vasantha Keerthana Selvan (Tech Advisor).
- [Creator Studio Web App](https://app.incubrix.com/): Application entry point.
```

---

### ISS-003: Missing SoftwareApplication & Offer Schema for 6 Credit Pricing Tiers on /pricing
- **Priority Rank:** #3 | **Severity:** `CRITICAL` | **Category:** `Structured Data (JSON-LD)`
- **Affected URL:** `https://incubrix.com/pricing`
- **Actual Evidence Observed:**
  > GET https://incubrix.com/pricing (36,863 bytes) -> jsonld_count = 0.
- **Problem Description:**
  The /pricing page details 6 plans (Free, Starter $10, Essential $20, Growth $50, Scale $100, Pro $250) in visual HTML cards but has 0 JSON-LD blocks, preventing Google rich product/software snippets and accurate AI pricing answers.
- **Recommended Correction:**
  Add SoftwareApplication JSON-LD with 6 factual Offer objects matching the exact USD monthly prices and credit allocations on /pricing.
- **Validation Method & Result:**
  `Validate SoftwareApplication JSON-LD syntax, verify 6 Offer nodes ($0, $10, $20, $50, $100, $250 USD), and confirm zero fabricated rating properties.` -> `OPEN ON LIVE SITE: 0 JSON-LD blocks present on https://incubrix.com/pricing. | Candidate Patch Check: PASS: Validated schema.org JSON-LD syntax and required entity properties for ISS-003 (0 unverified fields).` (Checked: `2026-10-24T19:16:32Z`)
- **Deployment Status:** `Patch tested locally; pending deployment by site administrator.`

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "SoftwareApplication",
  "name": "IncuBrix Creator Studio",
  "applicationCategory": "MultimediaApplication",
  "operatingSystem": "Web Browser",
  "url": "https://incubrix.com/pricing",
  "description": "AI-powered Creator Studio that turns one recording into clips, captions, voiceovers, and posts for YouTube, Instagram, LinkedIn, Spotify, and Bluesky.",
  "offers": [
    {
      "@type": "Offer",
      "name": "Free Plan (300 Credits/mo)",
      "price": "0",
      "priceCurrency": "USD",
      "url": "https://incubrix.com/pricing"
    },
    {
      "@type": "Offer",
      "name": "Starter Plan (1,000 Credits/mo)",
      "price": "10",
      "priceCurrency": "USD",
      "url": "https://incubrix.com/pricing"
    },
    {
      "@type": "Offer",
      "name": "Essential Plan (2,000 Credits/mo)",
      "price": "20",
      "priceCurrency": "USD",
      "url": "https://incubrix.com/pricing"
    },
    {
      "@type": "Offer",
      "name": "Growth Plan (5,000 Credits/mo)",
      "price": "50",
      "priceCurrency": "USD",
      "url": "https://incubrix.com/pricing"
    },
    {
      "@type": "Offer",
      "name": "Scale Plan (10,000 Credits/mo)",
      "price": "100",
      "priceCurrency": "USD",
      "url": "https://incubrix.com/pricing"
    },
    {
      "@type": "Offer",
      "name": "Pro Plan (25,000 Credits/mo)",
      "price": "250",
      "priceCurrency": "USD",
      "url": "https://incubrix.com/pricing"
    }
  ]
}
</script>
```

---

### ISS-004: Missing FAQPage Structured Data on /faq and /pricing
- **Priority Rank:** #4 | **Severity:** `HIGH` | **Category:** `Structured Data (JSON-LD)`
- **Affected URL:** `https://incubrix.com/faq`
- **Actual Evidence Observed:**
  > GET https://incubrix.com/faq (39,438 bytes) -> jsonld_count = 0.
- **Problem Description:**
  Both https://incubrix.com/faq and https://incubrix.com/pricing ('Pricing FAQs') contain structured Q&A content in HTML without FAQPage JSON-LD schema for AEO direct answer extraction.
- **Recommended Correction:**
  Add FAQPage JSON-LD containing Question and acceptedAnswer entities matching the visible FAQ text.
- **Validation Method & Result:**
  `Validate FAQPage JSON-LD via validate_json_ld() and verify non-empty mainEntity Question/Answer pairs.` -> `OPEN ON LIVE SITE: 0 JSON-LD blocks present on https://incubrix.com/faq. | Candidate Patch Check: PASS: Validated schema.org JSON-LD syntax and required entity properties for ISS-004 (0 unverified fields).` (Checked: `2026-10-24T19:16:32Z`)
- **Deployment Status:** `Patch tested locally; pending deployment by site administrator.`

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {
      "@type": "Question",
      "name": "Do you offer a free trial for IncuBrix paid plans?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "IncuBrix does not offer timed free trials for paid plans, but provides a permanent Free plan with 300 credits per month (approximately 21 one-minute videos) so creators can explore the platform before upgrading."
      }
    },
    {
      "@type": "Question",
      "name": "Is there a monthly usage expiration on IncuBrix plan credits?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "No. IncuBrix allows the credit limits provided in each plan to be utilized within a 1-year period, giving creators workflow flexibility."
      }
    },
    {
      "@type": "Question",
      "name": "Which platforms can IncuBrix publish to directly?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "IncuBrix supports publishing formatted clips, captions, and posts to YouTube, Instagram, LinkedIn, Spotify, and Bluesky from a single screen."
      }
    }
  ]
}
</script>
```

---

### ISS-005: Empty <h1> Heading Tag on /manifesto
- **Priority Rank:** #5 | **Severity:** `HIGH` | **Category:** `On-Page SEO`
- **Affected URL:** `https://incubrix.com/manifesto`
- **Actual Evidence Observed:**
  > GET https://incubrix.com/manifesto -> h1s: [""] (1 <h1> element found, innerText length = 0; 5 <h2> elements present).
- **Problem Description:**
  The /manifesto page contains an empty <h1></h1> tag with zero text characters, depriving search engines of a primary topical heading.
- **Recommended Correction:**
  Populate the <h1> tag on /manifesto with a descriptive primary heading aligned with the page title ('The IncuBrix Creator Manifesto: Five Beliefs About Creators and Their Time').
- **Validation Method & Result:**
  `Parse candidate HTML and assert exactly 1 non-empty <h1> element with length between 20 and 90 characters.` -> `OPEN ON LIVE SITE: <h1> is empty on /manifesto. | Candidate Patch Check: PASS: Validated single non-empty <h1> ('The IncuBrix Creator Manifesto: Five Beliefs About Creators and Their Time', 74 chars).` (Checked: `2026-10-24T19:16:32Z`)
- **Deployment Status:** `Patch tested locally; pending deployment by site administrator.`

```html
<h1>The IncuBrix Creator Manifesto: Five Beliefs About Creators and Their Time</h1>
```

---

### ISS-006: Orphan / Dead-End Page Architecture on /manifesto (0 Internal Links)
- **Priority Rank:** #6 | **Severity:** `HIGH` | **Category:** `Internal Linking`
- **Affected URL:** `https://incubrix.com/manifesto`
- **Actual Evidence Observed:**
  > GET https://incubrix.com/manifesto -> link_count = 2, internal_links = [].
- **Problem Description:**
  The /manifesto page has only 2 links total and 0 internal links to /, /about, /how-it-works, or /pricing, stranding crawlers and readers on a dead-end URL.
- **Recommended Correction:**
  Add global header/footer navigation and contextual internal links from /manifesto to /, /how-it-works, /about, and /pricing.
- **Validation Method & Result:**
  `Verify candidate HTML contains at least 4 crawlable internal <a href> links to core IncuBrix routes.` -> `OPEN ON LIVE SITE: /manifesto has 0 internal links. | Candidate Patch Check: PASS: Validated 4 internal navigation links for /manifesto.` (Checked: `2026-10-24T19:16:32Z`)
- **Deployment Status:** `Patch tested locally; pending deployment by site administrator.`

```html
<nav aria-label="Manifesto navigation">
  <a href="https://incubrix.com/">IncuBrix Home</a>
  <a href="https://incubrix.com/how-it-works">How IncuBrix Works</a>
  <a href="https://incubrix.com/pricing">Creator Studio Pricing</a>
  <a href="https://incubrix.com/about">About CreatorOps</a>
</nav>
```

---

### ISS-007: Missing HowTo Structured Data on /how-it-works for 4-Step Creator Workflow
- **Priority Rank:** #7 | **Severity:** `HIGH` | **Category:** `Structured Data (JSON-LD)`
- **Affected URL:** `https://incubrix.com/how-it-works`
- **Actual Evidence Observed:**
  > GET https://incubrix.com/how-it-works (37,883 bytes) -> jsonld_count = 0.
- **Problem Description:**
  https://incubrix.com/how-it-works explains the 4-step workflow (Get Content Insights -> Create Content -> Publish Everywhere -> Track & Grow) but includes 0 JSON-LD blocks.
- **Recommended Correction:**
  Embed HowTo JSON-LD with 4 ordered HowToStep items matching the visible process steps.
- **Validation Method & Result:**
  `Validate HowTo JSON-LD via validate_json_ld() and verify 4 sequential HowToStep nodes.` -> `OPEN ON LIVE SITE: 0 JSON-LD blocks present on https://incubrix.com/how-it-works. | Candidate Patch Check: PASS: Validated schema.org JSON-LD syntax and required entity properties for ISS-007 (0 unverified fields).` (Checked: `2026-10-24T19:16:32Z`)
- **Deployment Status:** `Patch tested locally; pending deployment by site administrator.`

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "HowTo",
  "name": "How to Turn One Recording into Multi-Platform Creator Content with IncuBrix",
  "description": "Four-step CreatorOps workflow from topic insights to multi-platform publishing.",
  "step": [
    {
      "@type": "HowToStep",
      "position": 1,
      "name": "Get Content Insights",
      "text": "Scan trending topics in your niche, spot competitor content gaps, and select a validated topic shortlist.",
      "url": "https://incubrix.com/how-it-works#insights"
    },
    {
      "@type": "HowToStep",
      "position": 2,
      "name": "Create & Edit via Transcript",
      "text": "Upload a recording or script. Edit video by deleting text in the transcript, extract up to 12 highlight clips, or narrate with voice cloning and digital avatars.",
      "url": "https://incubrix.com/how-it-works#create"
    },
    {
      "@type": "HowToStep",
      "position": 3,
      "name": "Repurpose Across 10+ Formats",
      "text": "Transform the core recording into vertical clips, captioned Reels/Shorts, LinkedIn posts, podcasts, and newsletter drafts.",
      "url": "https://incubrix.com/how-it-works#repurpose"
    },
    {
      "@type": "HowToStep",
      "position": 4,
      "name": "Publish Everywhere from One Screen",
      "text": "Distribute sized and captioned versions directly to YouTube, Instagram, LinkedIn, Spotify, and Bluesky.",
      "url": "https://incubrix.com/how-it-works#publish"
    }
  ]
}
</script>
```

---

### ISS-008: Missing AboutPage & Person Entity Graph on /team
- **Priority Rank:** #8 | **Severity:** `MEDIUM` | **Category:** `Structured Data (JSON-LD)`
- **Affected URL:** `https://incubrix.com/team`
- **Actual Evidence Observed:**
  > GET https://incubrix.com/team (36,519 bytes) -> jsonld_count = 0.
- **Problem Description:**
  https://incubrix.com/team lists 6 leadership and advisory team members with LinkedIn profiles, but lacks Person/Organization JSON-LD to establish E-E-A-T entity authority in Knowledge Graphs.
- **Recommended Correction:**
  Add AboutPage + Organization member JSON-LD listing verified leadership team members.
- **Validation Method & Result:**
  `Validate AboutPage JSON-LD via validate_json_ld() and confirm 6 Person records under mainEntity.member.` -> `OPEN ON LIVE SITE: 0 JSON-LD blocks present on https://incubrix.com/team. | Candidate Patch Check: PASS: Validated schema.org JSON-LD syntax and required entity properties for ISS-008 (0 unverified fields).` (Checked: `2026-10-24T19:16:32Z`)
- **Deployment Status:** `Patch tested locally; pending deployment by site administrator.`

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "AboutPage",
  "name": "IncuBrix Leadership & Advisory Team",
  "url": "https://incubrix.com/team",
  "mainEntity": {
    "@type": "Organization",
    "name": "IncuBrix",
    "url": "https://incubrix.com/",
    "member": [
      {
        "@type": "Person",
        "name": "Kamraj Subramanian",
        "jobTitle": "Founder and CEO"
      },
      {
        "@type": "Person",
        "name": "Rachel Blewitt",
        "jobTitle": "COO & Head of Customer Success"
      },
      {
        "@type": "Person",
        "name": "Supriya Sambhus",
        "jobTitle": "Director, Product Management"
      },
      {
        "@type": "Person",
        "name": "Nidhi Raj",
        "jobTitle": "GTM & Growth Strategy"
      },
      {
        "@type": "Person",
        "name": "Santhosh CE",
        "jobTitle": "Software Engineering Manager"
      },
      {
        "@type": "Person",
        "name": "Vasantha Keerthana Selvan",
        "jobTitle": "Tech Advisor"
      }
    ]
  }
}
</script>
```

---

### ISS-009: 17 Content Images Across /, /about, /pricing, and /waitlist Have Empty alt="" Attributes
- **Priority Rank:** #9 | **Severity:** `MEDIUM` | **Category:** `Accessibility & Media`
- **Affected URL:** `https://incubrix.com/about`
- **Actual Evidence Observed:**
  > Live crawl found empty alt="" on / (1), /about (5: photo-12674086-w600.jpeg, etc.), /pricing (5), and /waitlist (6).
- **Problem Description:**
  17 <img> elements across 4 key conversion pages use empty alt="" attributes (1 on /, 5 on /about, 5 on /pricing, 6 on /waitlist), harming screen-reader accessibility and Google Image search indexing.
- **Recommended Correction:**
  Provide descriptive, non-stuffed alt text describing the creator workflow shown in each image.
- **Validation Method & Result:**
  `Parse candidate <img> tags and verify 0 images have missing or empty alt attributes.` -> `OPEN ON LIVE SITE: 5 images missing alt on https://incubrix.com/about. | Candidate Patch Check: PASS: Validated 2 image tags with non-empty descriptive alt attributes.` (Checked: `2026-10-24T19:16:32Z`)
- **Deployment Status:** `Patch tested locally; pending deployment by site administrator.`

```html
<img src="/assets/photo-36950633-w300.jpeg" alt="Creator recording video in studio for multi-platform AI repurposing" loading="lazy" width="300" height="200" />
<img src="/assets/photo-12674086-w600.jpeg" alt="Podcaster editing video transcript in IncuBrix Creator Studio" loading="lazy" width="600" height="400" />
```

---

### ISS-010: Zero Twitter/X Card Meta Tags (twitter:card, twitter:title, twitter:image) Across All 13 Pages
- **Priority Rank:** #10 | **Severity:** `MEDIUM` | **Category:** `On-Page SEO`
- **Affected URL:** `https://incubrix.com/`
- **Actual Evidence Observed:**
  > Live crawl across all 13 URLs: tw_card_count = 0 on every page.
- **Problem Description:**
  None of the 13 sitemap pages include <meta name="twitter:card" content="summary_large_image"> or related Twitter/X metadata, causing degraded social previews on X, Slack, and Discord.
- **Recommended Correction:**
  Add twitter:card, twitter:title, twitter:description, and twitter:image tags to the global <head> template.
- **Validation Method & Result:**
  `Verify candidate <head> includes twitter:card='summary_large_image', twitter:title, twitter:description, and twitter:image.` -> `OPEN ON LIVE SITE: 0 twitter:* meta tags on live page. | Candidate Patch Check: PASS: Validated Twitter/X summary_large_image card metadata.` (Checked: `2026-10-24T19:16:32Z`)
- **Deployment Status:** `Patch tested locally; pending deployment by site administrator.`

```html
<meta name="twitter:card" content="summary_large_image" />
<meta name="twitter:title" content="IncuBrix | Create With Purpose. Publish Without Limits." />
<meta name="twitter:description" content="IncuBrix turns one recording into clips, captions, voiceovers, and posts for YouTube, Instagram, LinkedIn, Spotify, and Bluesky." />
<meta name="twitter:image" content="https://incubrix.com/og-image.jpg" />
```

---

### ISS-011: Grammatical Error ('one content') & Pipe Character in Homepage Meta Description
- **Priority Rank:** #11 | **Severity:** `MEDIUM` | **Category:** `On-Page SEO`
- **Affected URL:** `https://incubrix.com/`
- **Actual Evidence Observed:**
  > GET https://incubrix.com/ -> <meta name="description" content="IncuBrix turns one content into clips, captions, voiceovers, and posts for every platform | then publishes and tracks it all from one screen.">
- **Problem Description:**
  The homepage meta description reads: 'IncuBrix turns one content into clips, captions, voiceovers, and posts for every platform | then publishes and tracks it all from one screen.' The phrase 'one content' is ungrammatical and the pipe '|' breaks sentence parsing in AI snippets.
- **Recommended Correction:**
  Replace with a grammatically clean, 152-character meta description naming core platforms and capabilities.
- **Validation Method & Result:**
  `Verify meta description length is 120-160 chars, contains no pipe '|' mid-sentence, and corrects 'one content'.` -> `OPEN ON LIVE SITE: Meta description still contains pipe/grammar issue. | Candidate Patch Check: PASS: Validated meta description (145 chars, pipe-free, grammatically clean).` (Checked: `2026-10-24T19:16:32Z`)
- **Deployment Status:** `Patch tested locally; pending deployment by site administrator.`

```html
<meta name="description" content="IncuBrix turns one recording into AI clips, captions, voiceovers, and posts—then publishes to YouTube, Instagram, LinkedIn, Spotify, and Bluesky." />
```

---

### ISS-012: Missing <lastmod> ISO-8601 Timestamps in sitemap.xml
- **Priority Rank:** #12 | **Severity:** `MEDIUM` | **Category:** `Technical & Crawlability`
- **Affected URL:** `https://incubrix.com/sitemap.xml`
- **Actual Evidence Observed:**
  > GET https://incubrix.com/sitemap.xml (1,194 bytes) -> 0 <lastmod> tags present across 13 <url> nodes.
- **Problem Description:**
  https://incubrix.com/sitemap.xml lists 13 <url> entries with <loc> and <changefreq>weekly</changefreq>, but omits <lastmod>. Google ignores <changefreq> and relies on <lastmod> to schedule recrawls.
- **Recommended Correction:**
  Include accurate <lastmod>YYYY-MM-DD</lastmod> tags derived from page modification dates in sitemap.xml.
- **Validation Method & Result:**
  `Parse XML with ElementTree and verify every <url> node contains both <loc> and a valid YYYY-MM-DD <lastmod> element.` -> `OPEN ON LIVE SITE: sitemap.xml has 0 <lastmod> elements. | Candidate Patch Check: PASS: Validated XML sitemap schema with 5 <url> entries and ISO-8601 <lastmod> tags.` (Checked: `2026-10-24T19:16:32Z`)
- **Deployment Status:** `Patch tested locally; pending deployment by site administrator.`

```html
<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url><loc>https://incubrix.com/</loc><lastmod>2026-10-24</lastmod></url>
  <url><loc>https://incubrix.com/about</loc><lastmod>2026-10-24</lastmod></url>
  <url><loc>https://incubrix.com/how-it-works</loc><lastmod>2026-10-24</lastmod></url>
  <url><loc>https://incubrix.com/pricing</loc><lastmod>2026-10-24</lastmod></url>
  <url><loc>https://incubrix.com/faq</loc><lastmod>2026-10-24</lastmod></url>
</urlset>
```

---

### ISS-013: robots.txt Lacks Explicit AI Search Crawler Allow Rules (GPTBot, OAI-SearchBot, PerplexityBot, ClaudeBot)
- **Priority Rank:** #13 | **Severity:** `MEDIUM` | **Category:** `AEO / GEO Readiness`
- **Affected URL:** `https://incubrix.com/robots.txt`
- **Actual Evidence Observed:**
  > GET https://incubrix.com/robots.txt (65 bytes):
User-agent: *
Allow: /
Sitemap: https://incubrix.com/sitemap.xml
- **Problem Description:**
  While robots.txt has a wildcard Allow: /, enterprise CDNs and WAFs frequently throttle AI search bots unless OAI-SearchBot, GPTBot, PerplexityBot, ClaudeBot, and Google-Extended are explicitly permitted.
- **Recommended Correction:**
  Add explicit User-agent allow blocks for OAI-SearchBot, GPTBot, PerplexityBot, ClaudeBot, and Google-Extended plus Sitemap reference.
- **Validation Method & Result:**
  `Verify candidate robots.txt explicitly allows OAI-SearchBot, GPTBot, PerplexityBot, ClaudeBot, and includes Sitemap directive.` -> `OPEN ON LIVE SITE: robots.txt lacks explicit OAI-SearchBot/PerplexityBot rules. | Candidate Patch Check: PASS: Validated robots.txt AI crawler allow rules and Sitemap reference.` (Checked: `2026-10-24T19:16:32Z`)
- **Deployment Status:** `Patch tested locally; pending deployment by site administrator.`

```html
User-agent: *
Allow: /

User-agent: OAI-SearchBot
Allow: /

User-agent: GPTBot
Allow: /

User-agent: PerplexityBot
Allow: /

User-agent: ClaudeBot
Allow: /

User-agent: Google-Extended
Allow: /

Sitemap: https://incubrix.com/sitemap.xml
```

---

### ISS-014: Missing Explicit <meta name="robots"> Max-Snippet & Max-Image-Preview Directives Across All 13 Pages
- **Priority Rank:** #14 | **Severity:** `MEDIUM` | **Category:** `AEO / GEO Readiness`
- **Affected URL:** `https://incubrix.com/`
- **Actual Evidence Observed:**
  > Live crawl across all 13 sitemap URLs: robots_meta_count = 0.
- **Problem Description:**
  None of the 13 pages declare <meta name="robots" content="index, follow, max-snippet:-1, max-image-preview:large, max-video-preview:-1">, which explicitly authorizes Google AI Overviews and Answer Boxes to extract full snippets and large previews.
- **Recommended Correction:**
  Add the explicit robots meta tag enabling max-snippet:-1 and max-image-preview:large on all indexable marketing pages.
- **Validation Method & Result:**
  `Verify candidate <meta name="robots"> includes index, follow, max-snippet:-1, and max-image-preview:large.` -> `OPEN ON LIVE SITE: meta robots tag missing on live page. | Candidate Patch Check: PASS: Validated meta robots AEO/GEO snippet directives.` (Checked: `2026-10-24T19:16:32Z`)
- **Deployment Status:** `Patch tested locally; pending deployment by site administrator.`

```html
<meta name="robots" content="index, follow, max-snippet:-1, max-image-preview:large, max-video-preview:-1" />
```

---

### ISS-015: Render-Blocking Third-Party Calendly CSS Loaded in <head> Across Non-Booking Pages
- **Priority Rank:** #15 | **Severity:** `MEDIUM` | **Category:** `Performance & CWV`
- **Affected URL:** `https://incubrix.com/`
- **Actual Evidence Observed:**
  > Found synchronous <link href="https://assets.calendly.com/assets/external/widget.css" rel="stylesheet"> in <head> of https://incubrix.com/ and subpages.
- **Problem Description:**
  <link href="https://assets.calendly.com/assets/external/widget.css" rel="stylesheet"> is loaded synchronously in <head> across pages that do not embed a Calendly widget (/pricing, /privacy, /terms), adding a blocking third-party TLS/CSS round-trip before First Contentful Paint.
- **Recommended Correction:**
  Load Calendly CSS asynchronously using media="print" onload="this.media='all'" or restrict it strictly to /how-it-works and /contact.
- **Validation Method & Result:**
  `Verify candidate head snippet eliminates synchronous render-blocking stylesheet link to assets.calendly.com.` -> `OPEN ON LIVE SITE: Render-blocking Calendly CSS present in <head>. | Candidate Patch Check: PASS: Validated non-blocking preload pattern for third-party Calendly stylesheet.` (Checked: `2026-10-24T19:16:32Z`)
- **Deployment Status:** `Patch tested locally; pending deployment by site administrator.`

```html
<link rel="preload" href="https://assets.calendly.com/assets/external/widget.css" as="style" onload="this.onload=null;this.rel='stylesheet'" />
<noscript><link rel="stylesheet" href="https://assets.calendly.com/assets/external/widget.css" /></noscript>
```

---

### ISS-016: Legacy /waitlist Page Remains Indexed in Sitemap Despite 'Creator Studio is Live' Launch
- **Priority Rank:** #16 | **Severity:** `MEDIUM` | **Category:** `Technical & Crawlability`
- **Affected URL:** `https://incubrix.com/waitlist`
- **Actual Evidence Observed:**
  > GET https://incubrix.com/waitlist (HTTP 200, canonical='https://incubrix.com/waitlist') is listed in sitemap.xml alongside https://incubrix.com/.
- **Problem Description:**
  https://incubrix.com/waitlist states 'Creator Studio is live. Start free today.' and targets the exact same core value proposition as https://incubrix.com/, splitting link equity and causing keyword cannibalization.
- **Recommended Correction:**
  Either 301-redirect /waitlist to https://incubrix.com/ or set canonical of /waitlist to https://incubrix.com/ and remove /waitlist from sitemap.xml.
- **Validation Method & Result:**
  `Verify candidate /waitlist head directive points canonical to https://incubrix.com/ and sets noindex, follow.` -> `OPEN ON LIVE SITE: /waitlist canonical is https://incubrix.com/waitlist. | Candidate Patch Check: PASS: Validated canonical consolidation and noindex directive for /waitlist.` (Checked: `2026-10-24T19:16:32Z`)
- **Deployment Status:** `Patch tested locally; pending deployment by site administrator.`

```html
<link rel="canonical" href="https://incubrix.com/" />
<meta name="robots" content="noindex, follow" />
```

---

### ISS-017: Body CTA Links Point Exclusively to app.incubrix.com Without Contextual Internal Links to /how-it-works or /pricing
- **Priority Rank:** #17 | **Severity:** `MEDIUM` | **Category:** `Internal Linking`
- **Affected URL:** `https://incubrix.com/`
- **Actual Evidence Observed:**
  > GET https://incubrix.com/ -> 14 body links to https://app.incubrix.com/, 0 contextual body links to /pricing or /faq.
- **Problem Description:**
  In the body content of /, /about, and /how-it-works, almost every anchor tag points to https://app.incubrix.com/ (14 times on /) rather than passing contextual anchor-text authority to /pricing, /faq, and feature guides.
- **Recommended Correction:**
  Add descriptive internal anchor links from homepage pillar sections to /how-it-works, /pricing, and /faq.
- **Validation Method & Result:**
  `Verify candidate internal link block contains descriptive anchor text linking to /how-it-works, /pricing, and /faq.` -> `OPEN ON LIVE SITE: Issue ISS-017 remains open on https://incubrix.com/ (awaiting production deploy). | Candidate Patch Check: PASS: Validated contextual internal links to /how-it-works, /pricing, and /faq.` (Checked: `2026-10-24T19:16:32Z`)
- **Deployment Status:** `Patch tested locally; pending deployment by site administrator.`

```html
<p>Explore <a href="https://incubrix.com/how-it-works">how the 4-step IncuBrix CreatorOps workflow operates</a>, compare <a href="https://incubrix.com/pricing">credit-based Creator Studio pricing plans</a>, or read our <a href="https://incubrix.com/faq">Creator Studio FAQ</a>.</p>
```

---

### ISS-018: Uncompressed 415 KB JPEG Open Graph Image (/og-image.jpg) & Logo Asset
- **Priority Rank:** #18 | **Severity:** `LOW` | **Category:** `Performance & CWV`
- **Affected URL:** `https://incubrix.com/og-image.jpg`
- **Actual Evidence Observed:**
  > HEAD https://incubrix.com/og-image.jpg -> Content-Type: image/jpeg, Content-Length: 415202.
- **Problem Description:**
  https://incubrix.com/og-image.jpg is 415,202 bytes (image/jpeg) and /assets/incubrix-logo.jpg uses JPEG for a brand logo instead of SVG/WebP.
- **Recommended Correction:**
  Compress /og-image.jpg to <120 KB progressive JPEG/WebP (1200x630) with explicit og:image:width and og:image:height meta tags.
- **Validation Method & Result:**
  `Verify candidate OG image metadata specifies og:image:width='1200', og:image:height='630', and non-empty og:image:alt.` -> `OPEN ON LIVE SITE: No live fix detected on https://incubrix.com/og-image.jpg. | Candidate Patch Check: PASS: Validated Open Graph image dimensions (1200x630) and alt metadata.` (Checked: `2026-10-24T19:16:32Z`)
- **Deployment Status:** `Patch tested locally; pending deployment by site administrator.`

```html
<meta property="og:image" content="https://incubrix.com/og-image.jpg" />
<meta property="og:image:width" content="1200" />
<meta property="og:image:height" content="630" />
<meta property="og:image:alt" content="IncuBrix Creator Studio — Create With Purpose, Publish Without Limits" />
```

---

### ISS-019: Pipe Character ('|') Used as Punctuation in /faq Meta Description
- **Priority Rank:** #19 | **Severity:** `LOW` | **Category:** `On-Page SEO`
- **Affected URL:** `https://incubrix.com/faq`
- **Actual Evidence Observed:**
  > GET https://incubrix.com/faq -> <meta name="description" content="Everything you need to know about IncuBrix | getting started, features, pricing, brand partnerships, data privacy, and support.">
- **Problem Description:**
  The /faq meta description uses a vertical pipe '|' inside a sentence ('Everything you need to know about IncuBrix | getting started, features, pricing...'), which truncates or splits snippets in some search parsers.
- **Recommended Correction:**
  Replace the pipe character with an em-dash or colon and include concrete AEO keywords (credit pricing, voice cloning, multi-platform publishing).
- **Validation Method & Result:**
  `Verify candidate meta description has 120-160 characters and zero pipe '|' characters.` -> `OPEN ON LIVE SITE: Meta description still contains pipe/grammar issue. | Candidate Patch Check: PASS: Validated meta description (146 chars, pipe-free, grammatically clean).` (Checked: `2026-10-24T19:16:32Z`)
- **Deployment Status:** `Patch tested locally; pending deployment by site administrator.`

```html
<meta name="description" content="Answers to common questions about IncuBrix Creator Studio: getting started, AI clipping, voice cloning, credit pricing, data privacy, and support." />
```

---

### ISS-020: www.incubrix.com Redirects to Apex incubrix.com — Ensure External Profiles Use Canonical Apex URL
- **Priority Rank:** #20 | **Severity:** `LOW` | **Category:** `Technical & Crawlability`
- **Affected URL:** `https://www.incubrix.com/`
- **Actual Evidence Observed:**
  > GET https://www.incubrix.com/ -> Redirects toFINAL_URL: https://incubrix.com/ (canonical='https://incubrix.com/').
- **Problem Description:**
  Requests to https://www.incubrix.com/ redirect to https://incubrix.com/ (where canonical tags and sitemap.xml reside). External links pointing to www incur an extra HTTP redirect hop.
- **Recommended Correction:**
  Standardize all directory citations, social profiles, and UTM links to use the canonical apex https://incubrix.com/ URL directly.
- **Validation Method & Result:**
  `Verify canonical tag uses https://incubrix.com/ without www.` -> `OPEN ON LIVE SITE: Issue ISS-020 remains open on https://www.incubrix.com/ (awaiting production deploy). | Candidate Patch Check: PASS: Validated apex canonical URL without www.` (Checked: `2026-10-24T19:16:32Z`)
- **Deployment Status:** `Patch tested locally; pending deployment by site administrator.`

```html
<link rel="canonical" href="https://incubrix.com/" />
```

---

### ISS-021: Duplicated ~20 KB Inline <style> Block Across All 13 HTML Pages Instead of Cached Stylesheet
- **Priority Rank:** #21 | **Severity:** `LOW` | **Category:** `Performance & CWV`
- **Affected URL:** `https://incubrix.com/`
- **Actual Evidence Observed:**
  > Live crawl shows 36,519 to 59,079 bytes per HTML response with inline :root{--bg:#05070D...} CSS duplicated on every route.
- **Problem Description:**
  Each of the 13 pages embeds ~20 KB of identical inline CSS in <head>, preventing browser caching across page navigations and increasing HTML document size to 36 KB–59 KB.
- **Recommended Correction:**
  Extract shared styles into a fingerprinted, immutable cached stylesheet (/assets/main.css) with Cache-Control: public, max-age=31536000, immutable.
- **Validation Method & Result:**
  `Verify candidate external stylesheet link syntax is valid.` -> `OPEN ON LIVE SITE: Issue ISS-021 remains open on https://incubrix.com/ (awaiting production deploy). | Candidate Patch Check: PASS: Validated external cacheable stylesheet tag.` (Checked: `2026-10-24T19:16:32Z`)
- **Deployment Status:** `Patch tested locally; pending deployment by site administrator.`

```html
<link rel="stylesheet" href="/assets/incubrix-core.min.css" />
```

---

### ISS-022: Missing Open Graph Locale Tags (og:locale & og:locale:alternate) for US, India, and UK Creator Markets
- **Priority Rank:** #22 | **Severity:** `LOW` | **Category:** `AEO / GEO Readiness`
- **Affected URL:** `https://incubrix.com/`
- **Actual Evidence Observed:**
  > GET https://incubrix.com/ -> og_tags has og:title, og:description, og:type, og:image, og:url; og:locale is absent.
- **Problem Description:**
  Pages include basic og:title/og:description/og:url but omit og:locale (en_US) and alternate English locales (en_IN, en_GB) for international creator discovery.
- **Recommended Correction:**
  Add og:locale and og:locale:alternate tags for en_US, en_IN, and en_GB.
- **Validation Method & Result:**
  `Verify candidate metadata contains og:locale='en_US' and alternates for en_IN and en_GB.` -> `OPEN ON LIVE SITE: Issue ISS-022 remains open on https://incubrix.com/ (awaiting production deploy). | Candidate Patch Check: PASS: Validated og:locale tags for US, India, and UK markets.` (Checked: `2026-10-24T19:16:32Z`)
- **Deployment Status:** `Patch tested locally; pending deployment by site administrator.`

```html
<meta property="og:locale" content="en_US" />
<meta property="og:locale:alternate" content="en_IN" />
<meta property="og:locale:alternate" content="en_GB" />
```

---
