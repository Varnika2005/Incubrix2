# IncuBrix 90-Day Implementation & Launch Kit

**Target Company:** IncuBrix Private Limited (`https://www.incubrix.com`)  
**Assessment:** 2027 Graduate Hiring — Growth Engineer Assessment (Option 3)  
**Execution Window:** 90 Days (Weeks 1 through 12)  
**Total Estimated Budget:** \$1,270 USD  
**Target Results (Day 90):** +2,500 Monthly Organic Sign-Ups | 8+ Keywords in Top 5 Google Search | 5+ Google Answer Boxes | 25%+ Unprompted AI Assistant Recommendation Rate  

---

## 1. Executive Implementation Roadmap

```
Phase 1: Days 1–30                Phase 2: Days 31–60                 Phase 3: Days 61–90
Foundation & Technical AEO/SEO    Content Velocity & Entity Seeding   GEO Citation Scale & Multi-Market
------------------------------    ---------------------------------   ---------------------------------
W1: JSON-LD Graph & /llms.txt     W5: 6 New Content Studio Pages      W9: 15 Programmatic Guides
W2: On-Page SEO & Alt Text Fixes  W6: Automated Weekly Multi-Market   W10: Regional India & UK Optimization
W3: First 4 Guides & Comparisons  W7: Community Advocacy (Reddit/HN)  W11: Performance & CWV Sprint
W4: Tier-1 Directory Claiming     W8: Editorial Data PR (Buffer/Later)W12: 90-Day Readout & Q2 Roadmap
```

---

## 2. Phase 1: Days 1–30 — Foundation & Technical AEO/SEO

### Week 1 (LP-W01): Deploy Core JSON-LD Entity Graph & Root `/llms.txt`
- **Objective:** Establish machine-readable entity identity for IncuBrix across search crawlers and AI answer engines.
- **Actions:**
  1. Inject `Organization`, `WebSite`, and `SoftwareApplication` JSON-LD schemas into `https://incubrix.com/` (`ISS-001`).
  2. Deploy `SoftwareApplication` with 6 transparent credit pricing tiers ($0 to $250/mo) on `/pricing` (`ISS-003`).
  3. Deploy the validated `/llms.txt` markdown manifest to root (`ISS-002`).
  4. Submit updated sitemap and robots.txt (`ISS-012`, `ISS-013`) via Google Search Console.
- **Owner:** Growth Engineer & Frontend Tech Lead
- **Tools:** Git, Production CMS / Server, Google Search Console, Google Rich Results Test
- **Budget:** \$0.00
- **Baseline:** 0 JSON-LD schemas, HTTP 404 on `/llms.txt`.
- **Target:** 100% valid JSON-LD on all 13 sitemap URLs; `/llms.txt` returning HTTP 200.
- **Risks & Mitigation:** Production deploy freeze; mitigate by validating patches locally and providing drop-in `<script>` snippets.

### Week 2 (LP-W02): On-Page SEO, Heading Hierarchy, Accessibility & Canonical Fixes
- **Objective:** Eliminate crawl anomalies and improve technical indexing quality.
- **Actions:**
  1. Populate empty `<h1>` tag on `/manifesto` with target keyword (*"The CreatorOps Manifesto: Replacing Fragmented Tools with an Integrated AI Studio"*) (`ISS-005`).
  2. Add global header/footer navigation links to `/manifesto` to eliminate orphan page status (`ISS-006`).
  3. Populate descriptive `alt` attributes on 17 uncaptioned content images across `/`, `/about`, `/pricing`, `/waitlist` (`ISS-009`).
  4. Add missing Twitter/X card meta tags (`ISS-010`) and fix typographical error in homepage description (`ISS-011`).
  5. Add `<meta name="robots" content="noindex, follow">` to legacy `/waitlist` to eliminate keyword cannibalization (`ISS-016`).
- **Owner:** Technical SEO Specialist & Frontend Developer
- **Tools:** VS Code, Git, Screaming Frog SEO Spider
- **Budget:** \$0.00
- **Baseline:** Empty H1, orphan page, 17 missing alt tags.
- **Target:** 0 technical SEO warnings on Google Search Console; clean heading tree across all 13 URLs.
- **Risks & Mitigation:** Regression on mobile viewport; verify with responsive Playwright test suite.

### Week 3 (LP-W03): Publish First 4 High-Intent Comparison & How-To Guides
- **Objective:** Target immediate commercial comparison and problem-solving search queries.
- **Actions:**
  1. Publish `PAGE-001`: *How to Turn a 1-Hour Video into 12 Short Clips & Multi-Platform Posts with AI* (`/guides/how-to-turn-one-video-into-12-clips-and-multi-platform-posts`).
  2. Publish `PAGE-002`: *IncuBrix vs OpusClip vs Descript (2026): Which AI Creator Studio Fits Your Workflow?* (`/guides/incubrix-vs-opusclip-vs-descript-comparison`).
  3. Publish `PAGE-003`: *IncuBrix vs Repurpose.io vs Buffer: Best Multi-Platform Creator Publishing Workflow* (`/guides/incubrix-vs-repurpose-io-vs-buffer-multi-platform-publishing`).
  4. Publish `PAGE-004`: *How to Create Talking-Head Videos & Podcast Narration with AI Voice Cloning and Digital Avatars*.
- **Owner:** Content Strategist & Growth Engineer
- **Tools:** Markdown / Static Site Generator, Google Search Console URL Inspection
- **Budget:** \$150.00 (Editorial design assets)
- **Baseline:** 0 published guide pages; 0 organic comparison keywords ranked.
- **Target:** 4 pages indexed by Google within 72 hours; initial rankings within top 50.
- **Risks & Mitigation:** Slow indexing; mitigate by requesting manual re-indexing in Search Console and internal linking from homepage.

### Week 4 (LP-W04): Tier-1 Software Directory Entity Seeding
- **Objective:** Seed structured product consensus across authoritative directories that feed LLM retrieval (RAG).
- **Actions:**
  1. Claim and complete verified vendor profiles on G2 (`CIT-001`, `CIT-002`, `CIT-003`).
  2. Submit official product profiles on Capterra (`CIT-004`, `CIT-005`), AlternativeTo (`CIT-010`, `CIT-011`), and Product Hunt (`CIT-007`, `CIT-008`).
  3. Submit IncuBrix under task taxonomies on Futurepedia (`CIT-013`, `CIT-014`) and There's An AI For That (`CIT-015`).
  4. Submit `https://incubrix.com/llms.txt` to `llmstxt.org` adopter directory (`CIT-030`).
- **Owner:** Product Marketing / GTM Lead
- **Tools:** Vendor Dashboards, Stripe Billing Documentation, Product Screenshots
- **Budget:** \$0.00 (Organic free profiles)
- **Baseline:** Absent from all major software directories; 0 directory backlinks.
- **Target:** 15 claimed and approved vendor profiles with verified feature sets and pricing tiers.
- **Risks & Mitigation:** Directory approval turnaround (7–14 days); submit all applications simultaneously in Week 4.

---

## 3. Phase 2: Days 31–60 — Content Velocity & Entity Seeding

### Week 5 (LP-W05): Publish Remaining 6 Content Studio Pages
- **Objective:** Expand search footprint across creator glossaries, problem guides, and technical FAQs.
- **Actions:**
  1. Publish `PAGE-005`: *What is CreatorOps? The New Standard for Solo Creators and Video Podcasters*.
  2. Publish `PAGE-006`: *AI Video Repurposing: From Long-Form Recording to Multi-Platform Audience*.
  3. Publish `PAGE-007`: *The Solo Creator Second Job Crisis: Why Tool Fragmentation is Burning Out Video Creators*.
  4. Publish `PAGE-008`: *Podcast-to-Video Repurposing Guide: Grow Your Show on YouTube, Spotify, Reels & LinkedIn*.
  5. Publish `PAGE-009`: *AI Digital Talking-Head Avatars for Creators: Script-to-Video Studio Guide*.
  6. Publish `PAGE-010`: *2026 Creator FAQ: AI Video Clipping, Safe-Zone Captions & Multi-Platform Publishing*.
- **Owner:** Content Strategist & Product Manager
- **Tools:** CMS, Schema Validator, Image Compression (WebP)
- **Budget:** \$200.00
- **Baseline:** 4 published guides.
- **Target:** 10 live, fully indexed AEO/GEO pages with valid JSON-LD schemas.

### Week 6 (LP-W06): Activate Automated Weekly Multi-Market Visibility Runs
- **Objective:** Establish continuous visibility telemetry and automated variance monitoring across US, India, and UK.
- **Actions:**
  1. Configure Windows Task Scheduler / GitHub Actions to run `python -m engine.cli run-visibility --mode live --markets US,IN,GB --limit 100` every Monday at 08:00 UTC.
  2. Generate and distribute weekly markdown reporting (`python -m engine.cli generate-report`).
  3. Flag any provider-level mention drops (>5% week-over-week) for rapid investigation.
- **Owner:** Growth Engineer
- **Tools:** Visibility Engine CLI, Python 3, Cron / Windows Task Scheduler, Sendgrid / Slack Webhook
- **Budget:** \$120.00 (Gemini & Perplexity API query budget for 400 monthly checks)
- **Baseline:** Manual periodic execution.
- **Target:** 100% automated weekly collection across US, IN, GB with 0 duplicate records and saved telemetry.

### Week 7 (LP-W07): Community & Founder-Led Education on Reddit, Indie Hackers & Hacker News
- **Objective:** Seed organic creator discussions on platforms directly ingested by Google Search and ChatGPT.
- **Actions:**
  1. Share transparent breakdown of creator workflow benchmarks on `r/NewTubers` (`CIT-022`) and `r/podcasting` (`CIT-023`).
  2. Publish case study on Indie Hackers (`CIT-025`) detailing lessons learned building a 1-hour-to-12-clip CreatorOps studio.
  3. Participate in Ask HN / Show HN threads regarding modern `/llms.txt` adoption (`CIT-026`).
- **Owner:** Founder / Developer Advocate
- **Tools:** Community Accounts, Google Analytics 4 Referral Tracking
- **Budget:** \$0.00 (Authentic, policy-compliant participation; zero spam)
- **Baseline:** 0 community brand mentions.
- **Target:** 5 high-karma community threads indexing on Google for comparative creator queries.

### Week 8 (LP-W08): Editorial Data PR Outreach to Creator Publications
- **Objective:** Earn high-authority editorial citations from industry authorities (Buffer, Sprout Social, Later).
- **Actions:**
  1. Pitch original benchmark data from IncuBrix's 100-Question Creator Research Study to Buffer Library editors (`CIT-016`, `CIT-017`).
  2. Submit guest contribution on multi-network video distribution to Sprout Social Insights (`CIT-018`) and Later Blog (`CIT-019`).
  3. Publish Spotify video podcast formatting guidelines referencing Spotify for Creators resources (`CIT-021`).
- **Owner:** GTM & Growth Strategy Lead
- **Tools:** Email Outreach, Research Data Excerpts, Google Search Console
- **Budget:** \$250.00 (PR asset preparation and outreach collateral)
- **Baseline:** 0 editorial citations.
- **Target:** 2 confirmed editorial backlinks / citations in authoritative creator marketing guides.

---

## 4. Phase 3: Days 61–90 — GEO Citation Scale & Multi-Market Expansion

### Week 9 (LP-W09): Expand Content Studio with 15 Programmatic Workflow Guides
- **Objective:** Scale long-tail question capture using the programmatic Brief Generator (`engine/cli.py generate-brief`).
- **Actions:**
  1. Generate briefs for 15 remaining high-priority questions (`Q-021` through `Q-035`).
  2. Batch-produce programmatic guides targeting specific format transformations (e.g. *Audio Podcast to LinkedIn Carousel*, *Webinar to 15 TikTok Clips*).
  3. Auto-inject `HowTo` schema and canonical cross-links.
- **Owner:** Content Strategist & Growth Engineer
- **Tools:** Engine Brief Generator, Markdown Exporter, Node.js Batch Renderer
- **Budget:** \$300.00
- **Baseline:** 10 published pages.
- **Target:** 25 live guide pages; +1,200 monthly organic search impressions.

### Week 10 (LP-W10): Localized Creator Market Optimization (India & UK)
- **Objective:** Optimize visibility for non-US markets where creator growth is surging.
- **Actions:**
  1. Tailor pricing communication to reflect local purchasing parity (e.g. INR pricing equivalent via Stripe on `en-IN` views).
  2. Optimize metadata and Open Graph locale tags (`og:locale: en_IN`, `og:locale: en_GB`) (`ISS-022`).
  3. Publish localized case studies featuring Indian and British creator workflows.
- **Owner:** Growth Engineer & Regional GTM Lead
- **Tools:** Next.js / Vite i18n routing, Google Search Console Geotargeting
- **Budget:** \$150.00
- **Baseline:** Visibility baseline tracking shows lower mention rate in India (en-IN) than US.
- **Target:** +50% increase in Indian and UK organic creator impressions; capture 3 localized Google PAA boxes.

### Week 11 (LP-W11): Core Web Vitals & Performance Engineering Sprint
- **Objective:** Achieve 95+ Mobile Google PageSpeed Insights score to support top-rank conversion.
- **Actions:**
  1. Defer third-party Calendly script loading using `async`/`defer` (`ISS-015`).
  2. Extract duplicated 20 KB inline CSS styles into external minified stylesheets with HTTP caching headers (`ISS-021`).
  3. Convert 415 KB uncompressed Open Graph image into 45 KB modern WebP format (`ISS-018`).
  4. Ensure Largest Contentful Paint (LCP) remains under 1.8 seconds on 4G mobile emulation.
- **Owner:** Frontend Performance Engineer
- **Tools:** Chrome DevTools Lighthouse, PageSpeed Insights API, Webpack / Vite Rollup
- **Budget:** \$0.00
- **Baseline:** Mobile LCP ~3.2s; render-blocking third-party CSS.
- **Target:** Mobile LCP < 2.0s; 0 render-blocking resources; 95+ Lighthouse score.

### Week 12 (LP-W12): 90-Day Readout, Attribution Audit & Q2 Roadmap
- **Objective:** Synthesize 90-day performance against baseline metrics and establish ongoing growth targets.
- **Actions:**
  1. Re-run complete 100-question multi-market visibility engine.
  2. Reconcile organic sign-ups and trial activations driven by AEO, SEO, and GEO channels.
  3. Present formal executive readout to leadership with recommendations for Q2 expansion.
- **Owner:** Growth Engineer & Leadership Team
- **Tools:** Visibility Engine, Google Analytics 4, Stripe Billing Metrics
- **Budget:** \$100.00
- **Target:** Complete attribution report validating ROI of the 90-day growth engine.

---

## 5. Budget, Resource Allocation & Risk Governance

### 90-Day Budget Allocation Summary

| Phase | Activities | Owner | Budget (USD) |
| :--- | :--- | :--- | :--- |
| **Days 1–30** | Technical fixes (`ISS-001..022`), `/llms.txt`, 4 guides, directory claims | Growth Engineer & Tech Lead | **\$150.00** |
| **Days 31–60** | 6 pages, automated visibility collection, community PR, editorial outreach | Content Lead & Growth Engineer | **\$570.00** |
| **Days 61–90** | 15 programmatic pages, India/UK localization, CWV sprint, final readout | Performance Engineer & GTM Lead | **\$550.00** |
| **Total 90-Day Budget** | *Full End-to-End Implementation* | | **\$1,270.00** |

### Key Risks & Mitigation Playbook

| Risk Scenario | Probability | Impact | Mitigation Strategy |
| :--- | :--- | :--- | :--- |
| **Production Access Delay:** IncuBrix engineering team delays deploying JSON-LD patches or `/llms.txt` to production. | Medium | High | All 22 patches are delivered as standalone, verified drop-in text artifacts (`data/patches/ISS-*.patch.txt`) with exact line numbers and pre-tested syntax. Zero refactoring required. |
| **Directory Verification Delay:** Review platforms (G2, Capterra) take 2+ weeks to approve new software listings. | High | Medium | Submit all 15 directory applications in parallel during Week 4, backed by verified Stripe pricing documentation and product screenshots. |
| **AI Assistant Answer Variance:** Gemini, ChatGPT, and Perplexity answers fluctuate across consecutive runs. | High | Low | Enforced two-pass verification rule (`pass_number >= 2`) with saved JSON evidence; only consensus observations count toward official metrics. |
| **Competitor Content Response:** Descript or OpusClip publish competing guides targeting identical keywords. | Medium | Medium | Maintain differentiation around IncuBrix's unique multi-format capabilities: pre-recording Content Insights, voice cloning, digital avatars, and native 5-platform publishing (Spotify & Bluesky). |

