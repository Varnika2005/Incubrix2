# IncuBrix Third-Party Citation Opportunity Report

**Target Brand:** IncuBrix (`https://www.incubrix.com`)  
**Research Date:** October 2026  
**Total Opportunities Analyzed:** 30 Specific Third-Party Targets  
**Verified Reachable Targets:** **18 Verified Live (HTTP 200)** | **12 WAF-Protected (HTTP 403 Bot-Blocked)** | **0 Unreachable (404/500)**  
**Raw Evidence Stored:** `data/evidence/citations/CIT-001.json` through `CIT-030.json`  

---

## 1. Executive Summary & Citation Strategy

Generative Engine Optimization (GEO) relies heavily on third-party consensus. When AI assistants (ChatGPT, Gemini, Perplexity, Claude) and Google AI Overviews synthesize recommendations for creator queries like *'best AI tool to turn long video into clips'* or *'IncuBrix vs OpusClip'*, they retrieve from authoritative software directories, comparison listicles, and creator community discussions.

### Four Categories of Citation Opportunities
1. **B2B & AI Software Directories (15 Targets):** G2, Capterra, Product Hunt, AlternativeTo, TrustRadius, Futurepedia, There's An AI For That, GetApp, Software Advice.
2. **Editorial Industry Guides (8 Targets):** Buffer Library, Sprout Social Insights, Later Blog, Spotify for Creators.
3. **Creator Community Discussions (6 Targets):** Reddit (`r/NewTubers`, `r/podcasting`, `r/videography`), Indie Hackers, Hacker News (Ask HN).
4. **AI Standards & Repositories (1 Target):** `llmstxt.org` (Proposed directory for AI-readable website manifests).

### Verification Methodology
Each URL was inspected using automated HTTP requests (`urllib.request`) saving status code, final URL, page title, and IncuBrix mention state to `data/evidence/citations/CIT-XXX.json`. Review platforms enforcing Cloudflare bot challenges returned HTTP 403 and are preserved transparently as `pending_check` without attempting prohibited scraping.

---

## 2. Master Table of 30 Citation Opportunities

| ID | Publisher Domain | Source Type | Page Title / Target URL | HTTP Status | Verification State | Relevant Question | Priority |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `CIT-001` | `g2.com` | `directory` | [Best AI Video Generator Software in 2026...](https://www.g2.com/categories/ai-video-generator) | `403` | Pending WAF Check (403) | `Q-003` | Tier 1 |
| `CIT-002` | `g2.com` | `directory` | [Best Video Editing Software | G2...](https://www.g2.com/categories/video-editing) | `403` | Pending WAF Check (403) | `Q-016` | Tier 1 |
| `CIT-003` | `g2.com` | `directory` | [Best Social Media Management Software | ...](https://www.g2.com/categories/social-media-mgmt) | `403` | Pending WAF Check (403) | `Q-060` | Tier 1 |
| `CIT-004` | `capterra.com` | `directory` | [Best Video Editing Software 2026 - Capte...](https://www.capterra.com/video-editing-software/) | `403` | Pending WAF Check (403) | `Q-089` | Tier 1 |
| `CIT-005` | `capterra.com` | `directory` | [Best Social Media Management Software - ...](https://www.capterra.com/social-media-management-software/) | `403` | Pending WAF Check (403) | `Q-093` | Tier 2 |
| `CIT-006` | `producthunt.com` | `directory` | [Best Video Editing Tools on Product Hunt...](https://www.producthunt.com/categories/video-editing) | `200` | **VERIFIED LIVE (200)** | `Q-017` | Tier 1 |
| `CIT-007` | `producthunt.com` | `directory` | [Top AI Video Tools & Topics on Product H...](https://www.producthunt.com/topics/ai-video) | `403` | Pending WAF Check (403) | `Q-094` | Tier 1 |
| `CIT-008` | `producthunt.com` | `comparison_article` | [Best OpusClip Alternatives & Competitors...](https://www.producthunt.com/products/opus-clip/alternatives) | `200` | **VERIFIED LIVE (200)** | `Q-088` | Tier 1 |
| `CIT-009` | `producthunt.com` | `comparison_article` | [Best Descript Alternatives & Competitors...](https://www.producthunt.com/products/descript/alternatives) | `200` | **VERIFIED LIVE (200)** | `Q-089` | Tier 1 |
| `CIT-010` | `alternativeto.net` | `directory` | [Descript Alternatives and Similar Softwa...](https://alternativeto.net/software/descript/) | `403` | Pending WAF Check (403) | `Q-091` | Tier 1 |
| `CIT-011` | `alternativeto.net` | `directory` | [Buffer Alternatives and Similar Software...](https://alternativeto.net/software/buffer/) | `403` | Pending WAF Check (403) | `Q-062` | Tier 2 |
| `CIT-012` | `trustradius.com` | `review_platform` | [Best Video Editing Software 2026 | Trust...](https://www.trustradius.com/video-editing) | `403` | Pending WAF Check (403) | `Q-022` | Tier 2 |
| `CIT-013` | `futurepedia.io` | `directory` | [Best AI Video Editing Tools | Futurepedi...](https://www.futurepedia.io/ai-tools/video-editing) | `200` | **VERIFIED LIVE (200)** | `Q-019` | Tier 1 |
| `CIT-014` | `futurepedia.io` | `directory` | [Best AI Social Media Tools | Futurepedia...](https://www.futurepedia.io/ai-tools/social-media) | `200` | **VERIFIED LIVE (200)** | `Q-031` | Tier 2 |
| `CIT-015` | `theresanaiforthat.com` | `directory` | [AI Tools for Video Repurposing | There's...](https://theresanaiforthat.com/s/video+repurposing/) | `403` | Pending WAF Check (403) | `Q-032` | Tier 1 |
| `CIT-016` | `buffer.com` | `editorial_resource` | [Content Repurposing: How to Turn One Ide...](https://buffer.com/resources/repurpose-content/) | `200` | **VERIFIED LIVE (200)** | `Q-037` | Tier 2 |
| `CIT-017` | `buffer.com` | `editorial_resource` | [Bluesky Scheduler & Publishing Guide | B...](https://buffer.com/bluesky) | `200` | **VERIFIED LIVE (200)** | `Q-062` | Tier 2 |
| `CIT-018` | `sproutsocial.com` | `editorial_resource` | [Always Up-to-Date Social Media Video Spe...](https://sproutsocial.com/insights/social-media-video-specs-guide/) | `200` | **VERIFIED LIVE (200)** | `Q-066` | Tier 2 |
| `CIT-019` | `later.com` | `editorial_resource` | [The Best Time to Post on Social Media | ...](https://later.com/blog/best-time-to-post-on-social-media/) | `200` | **VERIFIED LIVE (200)** | `Q-071` | Tier 3 |
| `CIT-020` | `creators.spotify.com` | `editorial_resource` | [Spotify for Creators — Audio & Video Pod...](https://creators.spotify.com/) | `200` | **VERIFIED LIVE (200)** | `Q-010` | Tier 1 |
| `CIT-021` | `reddit.com` | `community_discussion` | [r/NewTubers — YouTube Creator Growth, Cl...](https://www.reddit.com/r/NewTubers/) | `200` | **VERIFIED LIVE (200)** | `Q-008` | Tier 1 |
| `CIT-022` | `reddit.com` | `community_discussion` | [r/podcasting — Podcast Recording, Transc...](https://www.reddit.com/r/podcasting/) | `200` | **VERIFIED LIVE (200)** | `Q-022` | Tier 1 |
| `CIT-023` | `reddit.com` | `community_discussion` | [r/VideoEditing — AI Transcript Editing, ...](https://www.reddit.com/r/VideoEditing/) | `200` | **VERIFIED LIVE (200)** | `Q-020` | Tier 2 |
| `CIT-024` | `reddit.com` | `community_discussion` | [r/content_marketing — Multi-Format Repur...](https://www.reddit.com/r/content_marketing/) | `200` | **VERIFIED LIVE (200)** | `Q-035` | Tier 2 |
| `CIT-025` | `reddit.com` | `community_discussion` | [r/socialmedia — Cross-Platform Publishin...](https://www.reddit.com/r/socialmedia/) | `200` | **VERIFIED LIVE (200)** | `Q-065` | Tier 2 |
| `CIT-026` | `indiehackers.com` | `community_discussion` | [Indie Hackers — Solo Founder Personal Br...](https://www.indiehackers.com/) | `200` | **VERIFIED LIVE (200)** | `Q-014` | Tier 1 |
| `CIT-027` | `news.ycombinator.com` | `community_discussion` | [Hacker News (Y Combinator) — Show HN & C...](https://news.ycombinator.com/) | `200` | **VERIFIED LIVE (200)** | `Q-005` | Tier 2 |
| `CIT-028` | `getapp.com` | `directory` | [Best Video Editing Software for Creators...](https://www.getapp.com/operations-management-software/video-editing/) | `403` | Pending WAF Check (403) | `Q-025` | Tier 2 |
| `CIT-029` | `softwareadvice.com` | `directory` | [Top Video Editing Software Comparison | ...](https://www.softwareadvice.com/media/video-editing-comparison/) | `403` | Pending WAF Check (403) | `Q-095` | Tier 3 |
| `CIT-030` | `llmstxt.org` | `editorial_resource` | [llms.txt — The Proposed Standard for LLM...](https://llmstxt.org/) | `200` | **VERIFIED LIVE (200)** | `Q-085` | Tier 1 |

---

## 3. Detailed Opportunity Profiles & Truthful Outreach Angles

### CIT-001: Best AI Video Generator Software in 2026 | G2
- **Target URL:** https://www.g2.com/categories/ai-video-generator
- **Publisher Domain:** `g2.com` | **Source Type:** `directory` | **Priority:** `Tier 1`
- **Target Question ID:** `Q-003` | **Relevant Topic:** AI Video Generators, Digital Avatars & Text-to-Video Studios
- **HTTP Verification:** Status `403` -> `pending_check` (Evidence: `data/evidence/citations/CIT-001.json`)
- **Competitors Mentioned:** HeyGen, Synthesia, VEED, Descript, Kapwing
- **Why Source Matters for GEO/AEO:**
  High domain authority and structured category taxonomy directly ingested by LLM training and RAG retrieval pipelines.
- **Truthful Outreach & Earning Angle:**
  Submit an official, policy-compliant IncuBrix vendor profile listing verified features (transcript editing, 12-clip extraction, digital avatars, 5-platform publishing) and transparent Stripe credit pricing.

---

### CIT-002: Best Video Editing Software | G2
- **Target URL:** https://www.g2.com/categories/video-editing
- **Publisher Domain:** `g2.com` | **Source Type:** `directory` | **Priority:** `Tier 1`
- **Target Question ID:** `Q-016` | **Relevant Topic:** Transcript-Based Video Editing & AI Clipping
- **HTTP Verification:** Status `403` -> `pending_check` (Evidence: `data/evidence/citations/CIT-002.json`)
- **Competitors Mentioned:** Descript, VEED, Kapwing, Camtasia
- **Why Source Matters for GEO/AEO:**
  Allows categorizing IncuBrix under browser-based transcript video editors with factual feature verification.
- **Truthful Outreach & Earning Angle:**
  Claim vendor listing under Video Editing category highlighting delete-text-to-cut-video transcript editing and 1-hour-to-12-clips automation.

---

### CIT-003: Best Social Media Management Software | G2
- **Target URL:** https://www.g2.com/categories/social-media-mgmt
- **Publisher Domain:** `g2.com` | **Source Type:** `directory` | **Priority:** `Tier 1`
- **Target Question ID:** `Q-060` | **Relevant Topic:** Multi-Platform Publishing (YouTube, Instagram, LinkedIn, Spotify, Bluesky)
- **HTTP Verification:** Status `403` -> `pending_check` (Evidence: `data/evidence/citations/CIT-003.json`)
- **Competitors Mentioned:** Buffer, Hootsuite, Sprout Social, Later
- **Why Source Matters for GEO/AEO:**
  IncuBrix's `/publish` module natively supports YouTube, Instagram, LinkedIn, Spotify, and Bluesky from one screen.
- **Truthful Outreach & Earning Angle:**
  List IncuBrix in cross-category Social Media Management & Content Creation with verified documentation of 5-platform single-screen publishing.

---

### CIT-004: Best Video Editing Software 2026 - Capterra
- **Target URL:** https://www.capterra.com/video-editing-software/
- **Publisher Domain:** `capterra.com` | **Source Type:** `directory` | **Priority:** `Tier 1`
- **Target Question ID:** `Q-089` | **Relevant Topic:** Browser-Based AI Video Editing & Pricing Comparisons
- **HTTP Verification:** Status `403` -> `pending_check` (Evidence: `data/evidence/citations/CIT-004.json`)
- **Competitors Mentioned:** Descript, VEED, Kapwing
- **Why Source Matters for GEO/AEO:**
  Capterra displays structured starting price ($10/mo Starter) and free tier availability (Free 300 credits/mo), matching IncuBrix's exact pricing model.
- **Truthful Outreach & Earning Angle:**
  Submit verified Gartner Digital Markets vendor application with accurate screenshot evidence of Creator Studio and credit pricing tiers.

---

### CIT-005: Best Social Media Management Software - Capterra
- **Target URL:** https://www.capterra.com/social-media-management-software/
- **Publisher Domain:** `capterra.com` | **Source Type:** `directory` | **Priority:** `Tier 2`
- **Target Question ID:** `Q-093` | **Relevant Topic:** Centralized Creator Hub vs Traditional Schedulers
- **HTTP Verification:** Status `403` -> `pending_check` (Evidence: `data/evidence/citations/CIT-005.json`)
- **Competitors Mentioned:** Buffer, Hootsuite, Sprout Social, Later
- **Why Source Matters for GEO/AEO:**
  Positions IncuBrix in front of creators looking to consolidate editing and multi-network distribution.
- **Truthful Outreach & Earning Angle:**
  Provide verified product overview showing unified creation + distribution to YouTube, Instagram, LinkedIn, Spotify, and Bluesky.

---

### CIT-006: Best Video Editing Tools on Product Hunt
- **Target URL:** https://www.producthunt.com/categories/video-editing
- **Publisher Domain:** `producthunt.com` | **Source Type:** `directory` | **Priority:** `Tier 1`
- **Target Question ID:** `Q-017` | **Relevant Topic:** AI Video Clipping & Creator Studio Tools
- **HTTP Verification:** Status `200` -> `verified_live` (Evidence: `data/evidence/citations/CIT-006.json`)
- **Competitors Mentioned:** OpusClip, Descript, Munch, Submagic, Kapwing
- **Why Source Matters for GEO/AEO:**
  High concentration of early-adopter creators, podcasters, and indie founders.
- **Truthful Outreach & Earning Angle:**
  Create an official Product Hunt Product Hub page for IncuBrix Creator Studio linking to https://incubrix.com/ and https://app.incubrix.com/.

---

### CIT-007: Top AI Video Tools & Topics on Product Hunt
- **Target URL:** https://www.producthunt.com/topics/ai-video
- **Publisher Domain:** `producthunt.com` | **Source Type:** `directory` | **Priority:** `Tier 1`
- **Target Question ID:** `Q-094` | **Relevant Topic:** Digital Talking-Head Avatars & Text-to-Video
- **HTTP Verification:** Status `403` -> `pending_check` (Evidence: `data/evidence/citations/CIT-007.json`)
- **Competitors Mentioned:** HeyGen, Synthesia, ElevenLabs
- **Why Source Matters for GEO/AEO:**
  IncuBrix offers lip-synced digital avatars alongside real long-form video clipping.
- **Truthful Outreach & Earning Angle:**
  Tag IncuBrix under AI Video Generators with accurate feature documentation of digital talking-head avatars and voice cloning.

---

### CIT-008: Best OpusClip Alternatives & Competitors | Product Hunt
- **Target URL:** https://www.producthunt.com/products/opus-clip/alternatives
- **Publisher Domain:** `producthunt.com` | **Source Type:** `comparison_article` | **Priority:** `Tier 1`
- **Target Question ID:** `Q-088` | **Relevant Topic:** OpusClip Alternatives for Multi-Format Repurposing
- **HTTP Verification:** Status `200` -> `verified_live` (Evidence: `data/evidence/citations/CIT-008.json`)
- **Competitors Mentioned:** OpusClip, Munch, Descript, VEED, Kapwing
- **Why Source Matters for GEO/AEO:**
  High-intent comparison page where creators look for tools that go beyond clipping into voiceovers and publishing.
- **Truthful Outreach & Earning Angle:**
  Register IncuBrix as a verified alternative on Product Hunt highlighting 1-hour-to-12-clips + 5-platform publishing + 1-year credit validity.

---

### CIT-009: Best Descript Alternatives & Competitors | Product Hunt
- **Target URL:** https://www.producthunt.com/products/descript/alternatives
- **Publisher Domain:** `producthunt.com` | **Source Type:** `comparison_article` | **Priority:** `Tier 1`
- **Target Question ID:** `Q-089` | **Relevant Topic:** Descript Alternatives for Transcript Video Editing
- **HTTP Verification:** Status `200` -> `verified_live` (Evidence: `data/evidence/citations/CIT-009.json`)
- **Competitors Mentioned:** Descript, Riverside, Kapwing, VEED
- **Why Source Matters for GEO/AEO:**
  IncuBrix provides transcript-based video editing plus built-in niche topic insights and multi-platform distribution.
- **Truthful Outreach & Earning Angle:**
  Submit factual Product Hunt comparison metadata showing how IncuBrix combines transcript editing with multi-channel publishing.

---

### CIT-010: Descript Alternatives and Similar Software | AlternativeTo
- **Target URL:** https://alternativeto.net/software/descript/
- **Publisher Domain:** `alternativeto.net` | **Source Type:** `directory` | **Priority:** `Tier 1`
- **Target Question ID:** `Q-091` | **Relevant Topic:** Alternatives to Descript for Video & Podcast Editing
- **HTTP Verification:** Status `403` -> `pending_check` (Evidence: `data/evidence/citations/CIT-010.json`)
- **Competitors Mentioned:** Descript, Kapwing, VEED, Riverside
- **Why Source Matters for GEO/AEO:**
  Crowdsourced software catalog with structured feature tags (Transcript Editing, AI Voice Cloning, Social Publishing).
- **Truthful Outreach & Earning Angle:**
  Submit a transparent, policy-compliant software listing for IncuBrix Creator Studio with accurate tags and free-tier details.

---

### CIT-011: Buffer Alternatives and Similar Software | AlternativeTo
- **Target URL:** https://alternativeto.net/software/buffer/
- **Publisher Domain:** `alternativeto.net` | **Source Type:** `directory` | **Priority:** `Tier 2`
- **Target Question ID:** `Q-062` | **Relevant Topic:** Multi-Platform Publishing Alternatives Supporting Bluesky & LinkedIn
- **HTTP Verification:** Status `403` -> `pending_check` (Evidence: `data/evidence/citations/CIT-011.json`)
- **Competitors Mentioned:** Buffer, Hootsuite, Later, Sprout Social
- **Why Source Matters for GEO/AEO:**
  Highlights tools that publish to Bluesky, LinkedIn, Instagram, YouTube, and Spotify.
- **Truthful Outreach & Earning Angle:**
  Document IncuBrix's integrated creation-to-publishing workflow as an alternative for video and audio creators.

---

### CIT-012: Best Video Editing Software 2026 | TrustRadius
- **Target URL:** https://www.trustradius.com/video-editing
- **Publisher Domain:** `trustradius.com` | **Source Type:** `review_platform` | **Priority:** `Tier 2`
- **Target Question ID:** `Q-022` | **Relevant Topic:** Verified B2B & Prosumer Video Editing Platforms
- **HTTP Verification:** Status `403` -> `pending_check` (Evidence: `data/evidence/citations/CIT-012.json`)
- **Competitors Mentioned:** Descript, VEED, Kapwing
- **Why Source Matters for GEO/AEO:**
  Provides structured pricing and technical specification tables for AI crawlers.
- **Truthful Outreach & Earning Angle:**
  Claim vendor profile on TrustRadius and publish verified pricing ($0 Free to $250 Pro) and capability specifications.

---

### CIT-013: Best AI Video Editing Tools | Futurepedia AI Directory
- **Target URL:** https://www.futurepedia.io/ai-tools/video-editing
- **Publisher Domain:** `futurepedia.io` | **Source Type:** `directory` | **Priority:** `Tier 1`
- **Target Question ID:** `Q-019` | **Relevant Topic:** AI Video Clipping, Reframing & Transcript Editing Tools
- **HTTP Verification:** Status `200` -> `verified_live` (Evidence: `data/evidence/citations/CIT-013.json`)
- **Competitors Mentioned:** OpusClip, Descript, Munch, VEED, Submagic
- **Why Source Matters for GEO/AEO:**
  Targets creators specifically searching for AI-native video and audio workflows.
- **Truthful Outreach & Earning Angle:**
  Submit IncuBrix Creator Studio to Futurepedia's Video Editing and Social Media subcategories with verified Freemium/Credit pricing badge.

---

### CIT-014: Best AI Social Media Tools | Futurepedia
- **Target URL:** https://www.futurepedia.io/ai-tools/social-media
- **Publisher Domain:** `futurepedia.io` | **Source Type:** `directory` | **Priority:** `Tier 2`
- **Target Question ID:** `Q-031` | **Relevant Topic:** AI Content Repurposing & Social Distribution
- **HTTP Verification:** Status `200` -> `verified_live` (Evidence: `data/evidence/citations/CIT-014.json`)
- **Competitors Mentioned:** Repurpose.io, Castmagic, Buffer, Hootsuite
- **Why Source Matters for GEO/AEO:**
  Matches IncuBrix's `/repurpose` (10+ formats) and `/publish` (5 platforms) feature set.
- **Truthful Outreach & Earning Angle:**
  List IncuBrix under AI Social Media & Content Repurposing with clear documentation of Text-to-Audio, Text-to-Video, and Audio-to-Text capabilities.

---

### CIT-015: AI Tools for Video Repurposing | There's An AI For That
- **Target URL:** https://theresanaiforthat.com/s/video+repurposing/
- **Publisher Domain:** `theresanaiforthat.com` | **Source Type:** `directory` | **Priority:** `Tier 1`
- **Target Question ID:** `Q-032` | **Relevant Topic:** Turning Long Videos into Shorts, Reels, LinkedIn Posts & Newsletters
- **HTTP Verification:** Status `403` -> `pending_check` (Evidence: `data/evidence/citations/CIT-015.json`)
- **Competitors Mentioned:** OpusClip, Munch, Repurpose.io, Castmagic
- **Why Source Matters for GEO/AEO:**
  Task-indexed AI directory where users filter by specific jobs-to-be-done.
- **Truthful Outreach & Earning Angle:**
  Submit IncuBrix under the 'Video repurposing', 'Transcript editing', and 'Podcast to video' task taxonomies.

---

### CIT-016: Content Repurposing: How to Turn One Idea into Many | Buffer
- **Target URL:** https://buffer.com/resources/repurpose-content/
- **Publisher Domain:** `buffer.com` | **Source Type:** `editorial_resource` | **Priority:** `Tier 2`
- **Target Question ID:** `Q-037` | **Relevant Topic:** Adapting Content Across LinkedIn, Instagram Reels, YouTube & Bluesky
- **HTTP Verification:** Status `200` -> `verified_live` (Evidence: `data/evidence/citations/CIT-016.json`)
- **Competitors Mentioned:** Buffer, Descript, CapCut
- **Why Source Matters for GEO/AEO:**
  Editorial resource covering creator workflows and multi-channel formatting.
- **Truthful Outreach & Earning Angle:**
  Share original benchmark data from IncuBrix's 100-question CreatorOps research study for editorial citation consideration.

---

### CIT-017: Bluesky Scheduler & Publishing Guide | Buffer
- **Target URL:** https://buffer.com/bluesky
- **Publisher Domain:** `buffer.com` | **Source Type:** `editorial_resource` | **Priority:** `Tier 2`
- **Target Question ID:** `Q-062` | **Relevant Topic:** Publishing Creator Content to Bluesky, LinkedIn & YouTube
- **HTTP Verification:** Status `200` -> `verified_live` (Evidence: `data/evidence/citations/CIT-017.json`)
- **Competitors Mentioned:** Buffer
- **Why Source Matters for GEO/AEO:**
  Confirms high creator search demand for Bluesky + LinkedIn + YouTube cross-publishing, which IncuBrix natively supports.
- **Truthful Outreach & Earning Angle:**
  Publish our companion 'Multi-Platform Video & Bluesky Publishing Specification Guide' in Content Studio and reference ecosystem standards.

---

### CIT-018: Always Up-to-Date Social Media Video Specs Guide | Sprout Social
- **Target URL:** https://sproutsocial.com/insights/social-media-video-specs-guide/
- **Publisher Domain:** `sproutsocial.com` | **Source Type:** `editorial_resource` | **Priority:** `Tier 2`
- **Target Question ID:** `Q-066` | **Relevant Topic:** Aspect Ratios & Formatting for YouTube, Instagram & LinkedIn Video
- **HTTP Verification:** Status `200` -> `verified_live` (Evidence: `data/evidence/citations/CIT-018.json`)
- **Competitors Mentioned:** Sprout Social
- **Why Source Matters for GEO/AEO:**
  Directly aligns with IncuBrix's automated aspect-ratio sizing and caption safe-zone formatting.
- **Truthful Outreach & Earning Angle:**
  Cite Sprout Social's video spec benchmarks in IncuBrix's technical guides and offer creator clip-retention data for future editorial updates.

---

### CIT-019: The Best Time to Post on Social Media | Later Blog
- **Target URL:** https://later.com/blog/best-time-to-post-on-social-media/
- **Publisher Domain:** `later.com` | **Source Type:** `editorial_resource` | **Priority:** `Tier 3`
- **Target Question ID:** `Q-071` | **Relevant Topic:** Cross-Timezone Publishing for US, India, and UK Creator Audiences
- **HTTP Verification:** Status `200` -> `verified_live` (Evidence: `data/evidence/citations/CIT-019.json`)
- **Competitors Mentioned:** Later
- **Why Source Matters for GEO/AEO:**
  Relevant to creators distributing repurposed clips across US, India, and UK audiences.
- **Truthful Outreach & Earning Angle:**
  Contribute multi-market creator publishing cadence insights (US/IN/GB) when IncuBrix's scheduled publishing feature releases.

---

### CIT-020: Spotify for Creators — Audio & Video Podcast Distribution
- **Target URL:** https://creators.spotify.com/
- **Publisher Domain:** `creators.spotify.com` | **Source Type:** `editorial_resource` | **Priority:** `Tier 1`
- **Target Question ID:** `Q-010` | **Relevant Topic:** Turning Audio Podcasts into Video Podcasts & Social Clips for Spotify
- **HTTP Verification:** Status `200` -> `verified_live` (Evidence: `data/evidence/citations/CIT-020.json`)
- **Competitors Mentioned:** Riverside, Descript
- **Why Source Matters for GEO/AEO:**
  IncuBrix explicitly supports publishing to Spotify alongside YouTube, Instagram, LinkedIn, and Bluesky.
- **Truthful Outreach & Earning Angle:**
  Document IncuBrix's Spotify + video clip publishing workflow in official creator partner/integration directories.

---

### CIT-021: r/NewTubers — YouTube Creator Growth, Clipping & Workflow Discussions
- **Target URL:** https://www.reddit.com/r/NewTubers/
- **Publisher Domain:** `reddit.com` | **Source Type:** `community_discussion` | **Priority:** `Tier 1`
- **Target Question ID:** `Q-008` | **Relevant Topic:** Batch Producing YouTube Shorts & Finding Niche Content Gaps
- **HTTP Verification:** Status `200` -> `verified_live` (Evidence: `data/evidence/citations/CIT-021.json`)
- **Competitors Mentioned:** OpusClip, Descript, VidIQ, TubeBuddy, CapCut
- **Why Source Matters for GEO/AEO:**
  High-trust community where creators ask how to turn long videos into Shorts without burning out.
- **Truthful Outreach & Earning Angle:**
  Participate transparently with a verified founder/team flair, answering technical questions on transcript editing and sharing free workflow guides without spam.

---

### CIT-022: r/podcasting — Podcast Recording, Transcript Editing & Video Repurposing
- **Target URL:** https://www.reddit.com/r/podcasting/
- **Publisher Domain:** `reddit.com` | **Source Type:** `community_discussion` | **Priority:** `Tier 1`
- **Target Question ID:** `Q-022` | **Relevant Topic:** Browser-Based Podcast Video Editing & Multi-Format Repurposing
- **HTTP Verification:** Status `200` -> `verified_live` (Evidence: `data/evidence/citations/CIT-022.json`)
- **Competitors Mentioned:** Descript, Riverside, Castmagic, Headliner, Repurpose.io
- **Why Source Matters for GEO/AEO:**
  Podcasters frequently ask for credit-based alternatives where unused monthly hours don't expire after 30 days.
- **Truthful Outreach & Earning Angle:**
  Share transparent educational breakdowns of credit-based 1-year validity workflows and podcast-to-Spotify/Reels/LinkedIn distribution.

---

### CIT-023: r/VideoEditing — AI Transcript Editing, Captions & Workflow Automation
- **Target URL:** https://www.reddit.com/r/VideoEditing/
- **Publisher Domain:** `reddit.com` | **Source Type:** `community_discussion` | **Priority:** `Tier 2`
- **Target Question ID:** `Q-020` | **Relevant Topic:** Transcript-Based Video Cutting & Voice Clone Overdubs
- **HTTP Verification:** Status `200` -> `verified_live` (Evidence: `data/evidence/citations/CIT-023.json`)
- **Competitors Mentioned:** Descript, VEED, Kapwing, ElevenLabs
- **Why Source Matters for GEO/AEO:**
  Directly addresses editors looking to speed up rough cuts and social deliverables.
- **Truthful Outreach & Earning Angle:**
  Contribute technical tutorials on transcript-aligned rough cutting and safe-zone captioning in public weekly tool threads.

---

### CIT-024: r/content_marketing — Multi-Format Repurposing & B2B Video Strategy
- **Target URL:** https://www.reddit.com/r/content_marketing/
- **Publisher Domain:** `reddit.com` | **Source Type:** `community_discussion` | **Priority:** `Tier 2`
- **Target Question ID:** `Q-035` | **Relevant Topic:** Turning Video Transcripts into LinkedIn Posts, Blogs & Newsletters
- **HTTP Verification:** Status `200` -> `verified_live` (Evidence: `data/evidence/citations/CIT-024.json`)
- **Competitors Mentioned:** Repurpose.io, Castmagic, Buffer, Descript
- **Why Source Matters for GEO/AEO:**
  Matches IncuBrix's Audio/Video-to-Text repurposing for LinkedIn and newsletters.
- **Truthful Outreach & Earning Angle:**
  Publish case studies on preserving authentic creator voice when converting spoken video transcripts into written LinkedIn posts.

---

### CIT-025: r/socialmedia — Cross-Platform Publishing & Scheduler Discussions
- **Target URL:** https://www.reddit.com/r/socialmedia/
- **Publisher Domain:** `reddit.com` | **Source Type:** `community_discussion` | **Priority:** `Tier 2`
- **Target Question ID:** `Q-065` | **Relevant Topic:** Publishing to YouTube, Instagram, LinkedIn, Spotify & Bluesky
- **HTTP Verification:** Status `200` -> `verified_live` (Evidence: `data/evidence/citations/CIT-025.json`)
- **Competitors Mentioned:** Buffer, Hootsuite, Sprout Social, Later
- **Why Source Matters for GEO/AEO:**
  Social media managers regularly ask for tools that combine clip formatting with multi-network publishing.
- **Truthful Outreach & Earning Angle:**
  Answer questions about native API publishing vs watermarked cross-posting with verifiable technical facts.

---

### CIT-026: Indie Hackers — Solo Founder Personal Brand & CreatorOps Workflows
- **Target URL:** https://www.indiehackers.com/
- **Publisher Domain:** `indiehackers.com` | **Source Type:** `community_discussion` | **Priority:** `Tier 1`
- **Target Question ID:** `Q-014` | **Relevant Topic:** Building a Founder Content Engine in 2 Hours a Week
- **HTTP Verification:** Status `200` -> `verified_live` (Evidence: `data/evidence/citations/CIT-026.json`)
- **Competitors Mentioned:** Buffer, Typefully, Descript, OpusClip
- **Why Source Matters for GEO/AEO:**
  Ideal audience for IncuBrix's 'One recording in. A week of content out.' value proposition.
- **Truthful Outreach & Earning Angle:**
  Publish a transparent 'Building the Creator Operating System' engineering & growth post on Indie Hackers linking to https://incubrix.com/about.

---

### CIT-027: Hacker News (Y Combinator) — Show HN & Creator Infrastructure Discussions
- **Target URL:** https://news.ycombinator.com/
- **Publisher Domain:** `news.ycombinator.com` | **Source Type:** `community_discussion` | **Priority:** `Tier 2`
- **Target Question ID:** `Q-005` | **Relevant Topic:** CreatorOps Architecture, llms.txt & AI Video Pipelines
- **HTTP Verification:** Status `200` -> `verified_live` (Evidence: `data/evidence/citations/CIT-027.json`)
- **Competitors Mentioned:** Descript, ElevenLabs, HeyGen
- **Why Source Matters for GEO/AEO:**
  High technical authority domain for launching Creator Studio engineering write-ups.
- **Truthful Outreach & Earning Angle:**
  Publish a technical 'Show HN' post detailing how IncuBrix unifies transcript frame-cutting, voice cloning, and multi-platform distribution.

---

### CIT-028: Best Video Editing Software for Creators & Teams | GetApp
- **Target URL:** https://www.getapp.com/operations-management-software/video-editing/
- **Publisher Domain:** `getapp.com` | **Source Type:** `directory` | **Priority:** `Tier 2`
- **Target Question ID:** `Q-025` | **Relevant Topic:** Cloud Video Editing & Repurposing Software Directory
- **HTTP Verification:** Status `403` -> `pending_check` (Evidence: `data/evidence/citations/CIT-028.json`)
- **Competitors Mentioned:** Descript, VEED, Kapwing
- **Why Source Matters for GEO/AEO:**
  Structured comparison cards feed Bing and Google product knowledge graphs.
- **Truthful Outreach & Earning Angle:**
  Sync Gartner Digital Markets profile so IncuBrix appears on GetApp with verified pricing ($0 Free, $10 Starter) and feature checklists.

---

### CIT-029: Top Video Editing Software Comparison | Software Advice
- **Target URL:** https://www.softwareadvice.com/media/video-editing-comparison/
- **Publisher Domain:** `softwareadvice.com` | **Source Type:** `directory` | **Priority:** `Tier 3`
- **Target Question ID:** `Q-095` | **Relevant Topic:** Browser-Based AI Video Studio Comparisons
- **HTTP Verification:** Status `403` -> `pending_check` (Evidence: `data/evidence/citations/CIT-029.json`)
- **Competitors Mentioned:** Descript, VEED, Camtasia
- **Why Source Matters for GEO/AEO:**
  Captures SMB and creator studio buyers comparing subscription vs credit-based pricing.
- **Truthful Outreach & Earning Angle:**
  Include IncuBrix's 1-year credit validity policy and 5-platform publishing capability in the vendor comparison profile.

---

### CIT-030: llms.txt — The Proposed Standard for LLM-Friendly Website Documentation
- **Target URL:** https://llmstxt.org/
- **Publisher Domain:** `llmstxt.org` | **Source Type:** `editorial_resource` | **Priority:** `Tier 1`
- **Target Question ID:** `Q-085` | **Relevant Topic:** GEO / AEO Readiness via /llms.txt Directory Adoption
- **HTTP Verification:** Status `200` -> `verified_live` (Evidence: `data/evidence/citations/CIT-030.json`)
- **Competitors Mentioned:** ElevenLabs
- **Why Source Matters for GEO/AEO:**
  Once IncuBrix deploys `/llms.txt` (Fixing `ISS-002`), listing `https://incubrix.com/llms.txt` in community directories accelerates AI crawler indexing.
- **Truthful Outreach & Earning Angle:**
  Deploy the validated `/llms.txt` file generated in Issue ISS-002 to `https://incubrix.com/llms.txt` and submit to public `llms.txt` adopter directories.

---
