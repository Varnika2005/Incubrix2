import os
import sqlite3
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

ROOT_DIR = Path(__file__).resolve().parent.parent
DEFAULT_DB_PATH = ROOT_DIR / "data" / "incubrix.db"
EVIDENCE_DIR = ROOT_DIR / "data" / "evidence"
EXPORTS_DIR = ROOT_DIR / "exports"


def get_db_path(custom_path: Optional[str] = None) -> Path:
    if custom_path:
        return Path(custom_path)
    env_path = os.environ.get("SQLITE_DB_PATH")
    if env_path:
        p = Path(env_path)
        return p if p.is_absolute() else (ROOT_DIR / p)
    return DEFAULT_DB_PATH


def get_connection(custom_path: Optional[str] = None) -> sqlite3.Connection:
    db_path = get_db_path(custom_path)
    db_path.parent.mkdir(parents=True, exist_ok=True)
    EVIDENCE_DIR.mkdir(parents=True, exist_ok=True)
    EXPORTS_DIR.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(db_path), timeout=30.0)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL;")
    conn.execute("PRAGMA foreign_keys=ON;")
    return conn


SCHEMA_SQL = """
-- 1. Research Questions (100+ Creator Queries with Provenance & Deduplication)
CREATE TABLE IF NOT EXISTS questions (
    id TEXT PRIMARY KEY,
    canonical_question TEXT NOT NULL,
    normalized_fingerprint TEXT NOT NULL UNIQUE,
    original_wording TEXT NOT NULL,
    category TEXT NOT NULL,
    search_intent TEXT NOT NULL,
    target_persona TEXT NOT NULL,
    source_url TEXT NOT NULL,
    source_type TEXT NOT NULL,
    collection_date TEXT NOT NULL,
    validation_status TEXT NOT NULL DEFAULT 'validated',
    validation_notes TEXT,
    priority_score INTEGER NOT NULL DEFAULT 80,
    target_markets_json TEXT NOT NULL DEFAULT '["US","IN","GB"]',
    provenance_sources_json TEXT NOT NULL DEFAULT '[]',
    duplicate_merge_count INTEGER NOT NULL DEFAULT 0,
    is_demo INTEGER NOT NULL DEFAULT 0,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);

-- 2. Engine Execution Runs (Audit Trail for Visibility & Crawl Runs)
CREATE TABLE IF NOT EXISTS engine_runs (
    run_id TEXT PRIMARY KEY,
    run_type TEXT NOT NULL, -- 'visibility_run', 'technical_audit', 'report_generation', 'seed_init'
    mode TEXT NOT NULL, -- 'live', 'test', 'manual_evidence', 'demo'
    status TEXT NOT NULL, -- 'running', 'completed', 'partial_failure', 'failed'
    markets_json TEXT NOT NULL DEFAULT '["US"]',
    providers_json TEXT NOT NULL DEFAULT '[]',
    questions_targeted INTEGER NOT NULL DEFAULT 0,
    observations_recorded INTEGER NOT NULL DEFAULT 0,
    verified_count INTEGER NOT NULL DEFAULT 0,
    failed_count INTEGER NOT NULL DEFAULT 0,
    skipped_unavailable_count INTEGER NOT NULL DEFAULT 0,
    duration_ms INTEGER NOT NULL DEFAULT 0,
    estimated_cost_usd REAL NOT NULL DEFAULT 0.0,
    log_summary_json TEXT NOT NULL DEFAULT '[]',
    started_at TEXT NOT NULL,
    completed_at TEXT
);

-- 3. Visibility Observations (Search & AI Assistant Responses per Question/Market/Date/Pass)
CREATE TABLE IF NOT EXISTS visibility_observations (
    observation_id TEXT PRIMARY KEY,
    run_id TEXT NOT NULL,
    question_id TEXT NOT NULL,
    query_text TEXT NOT NULL,
    provider TEXT NOT NULL, -- 'google_web', 'chatgpt', 'gemini', 'perplexity', 'claude'
    provider_model TEXT,
    market TEXT NOT NULL, -- 'US', 'IN', 'GB'
    location_setting TEXT NOT NULL, -- e.g. 'United States (en-US, gl=us, hl=en)'
    observation_date TEXT NOT NULL, -- YYYY-MM-DD
    pass_number INTEGER NOT NULL DEFAULT 1, -- Pass 1 or Pass 2+ for AI variance verification
    collection_status TEXT NOT NULL, -- 'verified_observation', 'pending_verification', 'not_collected', 'failed_collection', 'provider_unavailable', 'demo_observation'
    is_demo INTEGER NOT NULL DEFAULT 0,
    incubrix_mentioned INTEGER NOT NULL DEFAULT 0,
    incubrix_cited INTEGER NOT NULL DEFAULT 0,
    incubrix_citation_urls_json TEXT NOT NULL DEFAULT '[]',
    google_organic_rank INTEGER, -- NULL if not ranked or not Google provider
    answer_box_present INTEGER NOT NULL DEFAULT 0,
    answer_box_owner TEXT,
    ai_overview_present INTEGER NOT NULL DEFAULT 0,
    ai_overview_cites_incubrix INTEGER NOT NULL DEFAULT 0,
    competitors_mentioned_json TEXT NOT NULL DEFAULT '[]',
    citations_found_json TEXT NOT NULL DEFAULT '[]',
    response_snippet TEXT,
    raw_evidence_path TEXT,
    screenshot_path TEXT,
    error_message TEXT,
    latency_ms INTEGER NOT NULL DEFAULT 0,
    estimated_cost_usd REAL NOT NULL DEFAULT 0.0,
    observed_at TEXT NOT NULL,
    FOREIGN KEY (question_id) REFERENCES questions(id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_obs_question_market_date
ON visibility_observations(question_id, provider, market, observation_date, pass_number);

-- 4. Technical SEO / AEO / GEO Audit Findings & Prioritized Fixes (20+ Real Records)
CREATE TABLE IF NOT EXISTS technical_issues (
    issue_id TEXT PRIMARY KEY,
    page_url TEXT NOT NULL,
    category TEXT NOT NULL, -- 'Structured Data (JSON-LD)', 'AEO / GEO Readiness', 'On-Page SEO', 'Technical & Crawlability', 'Accessibility & Media', 'Performance & CWV', 'Internal Linking'
    severity TEXT NOT NULL, -- 'critical', 'high', 'medium', 'low'
    priority_rank INTEGER NOT NULL,
    title TEXT NOT NULL,
    description TEXT NOT NULL,
    actual_evidence TEXT NOT NULL,
    recommended_change TEXT NOT NULL,
    ready_to_apply_code TEXT NOT NULL,
    validation_method TEXT NOT NULL,
    validation_status TEXT NOT NULL DEFAULT 'open', -- 'validated', 'open', 'failed_validation', 'pending_retest'
    validation_result TEXT,
    last_checked_at TEXT NOT NULL
);

-- 5. Content Studio Pages (10 Publish-Ready Pages Targeting Validated Opportunities)
CREATE TABLE IF NOT EXISTS content_pages (
    page_id TEXT PRIMARY KEY,
    slug TEXT NOT NULL UNIQUE,
    content_type TEXT NOT NULL, -- 'how_to_guide', 'product_comparison', 'faq_page', 'glossary_entry', 'problem_solving_guide'
    title TEXT NOT NULL,
    meta_description TEXT NOT NULL,
    target_audience TEXT NOT NULL,
    search_intent TEXT NOT NULL,
    primary_topic TEXT NOT NULL,
    target_question_ids_json TEXT NOT NULL DEFAULT '[]',
    supporting_questions_json TEXT NOT NULL DEFAULT '[]',
    direct_answer_summary TEXT NOT NULL, -- First 2 sentences direct AEO answer
    body_markdown TEXT NOT NULL,
    headings_json TEXT NOT NULL DEFAULT '[]',
    citations_json TEXT NOT NULL DEFAULT '[]',
    internal_links_json TEXT NOT NULL DEFAULT '[]',
    json_ld_schema TEXT NOT NULL,
    verification_checklist_json TEXT NOT NULL DEFAULT '[]',
    unverified_claims_flagged_json TEXT NOT NULL DEFAULT '[]',
    word_count INTEGER NOT NULL DEFAULT 0,
    status TEXT NOT NULL DEFAULT 'ready_to_publish', -- 'draft', 'reviewed', 'ready_to_publish'
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);

-- 6. Citation Opportunities (30 Specific Third-Party Pages)
CREATE TABLE IF NOT EXISTS citation_opportunities (
    opportunity_id TEXT PRIMARY KEY,
    page_url TEXT NOT NULL UNIQUE,
    page_title TEXT NOT NULL,
    publisher_domain TEXT NOT NULL,
    source_type TEXT NOT NULL, -- 'directory', 'comparison_article', 'editorial_resource', 'community_discussion', 'review_platform'
    relevant_question_id TEXT,
    relevant_topic TEXT NOT NULL,
    evidence_of_relevance TEXT NOT NULL,
    competitor_mentions_json TEXT NOT NULL DEFAULT '[]',
    incubrix_currently_mentioned INTEGER NOT NULL DEFAULT 0,
    suitability_rationale TEXT NOT NULL,
    outreach_angle TEXT NOT NULL,
    priority_tier TEXT NOT NULL DEFAULT 'Tier 1',
    http_status_checked INTEGER,
    verification_status TEXT NOT NULL DEFAULT 'verified_live', -- 'verified_live', 'verified_indexed', 'pending_check', 'unreachable'
    research_date TEXT NOT NULL,
    notes TEXT
);

-- 7. Crawled Live Pages Cache (Real HTTP Crawl Snapshots of incubrix.com)
CREATE TABLE IF NOT EXISTS crawled_pages (
    url TEXT PRIMARY KEY,
    final_url TEXT NOT NULL,
    http_status INTEGER NOT NULL,
    redirect_chain_json TEXT NOT NULL DEFAULT '[]',
    load_time_ms INTEGER NOT NULL DEFAULT 0,
    page_size_bytes INTEGER NOT NULL DEFAULT 0,
    title TEXT,
    meta_description TEXT,
    canonical_url TEXT,
    meta_robots TEXT,
    viewport TEXT,
    h1_tags_json TEXT NOT NULL DEFAULT '[]',
    h2_tags_json TEXT NOT NULL DEFAULT '[]',
    json_ld_blocks_json TEXT NOT NULL DEFAULT '[]',
    og_tags_json TEXT NOT NULL DEFAULT '{}',
    twitter_tags_json TEXT NOT NULL DEFAULT '{}',
    images_total INTEGER NOT NULL DEFAULT 0,
    images_missing_alt INTEGER NOT NULL DEFAULT 0,
    internal_links_json TEXT NOT NULL DEFAULT '[]',
    external_links_json TEXT NOT NULL DEFAULT '[]',
    broken_links_json TEXT NOT NULL DEFAULT '[]',
    raw_evidence_file TEXT,
    crawled_at TEXT NOT NULL
);

-- 8. Weekly Reports & 90-Day Launch Plan Tasks
CREATE TABLE IF NOT EXISTS weekly_reports (
    report_id TEXT PRIMARY KEY,
    report_title TEXT NOT NULL,
    period_start TEXT NOT NULL,
    period_end TEXT NOT NULL,
    generated_at TEXT NOT NULL,
    metrics_snapshot_json TEXT NOT NULL,
    report_markdown TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS launch_plan_tasks (
    task_id TEXT PRIMARY KEY,
    phase TEXT NOT NULL, -- 'Days 1-30: Foundation & Technical AEO/SEO', 'Days 31-60: Content Velocity & Entity Seeding', 'Days 61-90: GEO Citation Scale & Multi-Market Expansion'
    week_number INTEGER NOT NULL,
    title TEXT NOT NULL,
    description TEXT NOT NULL,
    owner_role TEXT NOT NULL,
    tools_used TEXT NOT NULL,
    estimated_budget_usd REAL NOT NULL DEFAULT 0.0,
    baseline_metric TEXT NOT NULL,
    target_metric TEXT NOT NULL,
    measured_metric TEXT NOT NULL,
    dependencies TEXT NOT NULL,
    risk_and_mitigation TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'in_progress' -- 'completed', 'in_progress', 'planned'
);
"""


def init_schema(custom_path: Optional[str] = None) -> None:
    conn = get_connection(custom_path)
    try:
        conn.executescript(SCHEMA_SQL)
        conn.commit()
    finally:
        conn.close()


def now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
