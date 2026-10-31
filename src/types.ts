export type SectionId =
  | 'overview'
  | 'visibility'
  | 'audit'
  | 'content'
  | 'citations'
  | 'questions'
  | 'reports'
  | 'launch'
  | 'settings';

export interface OverviewMetrics {
  questions: {
    collected_total: number;
    validated_total: number;
    duplicates_merged_with_provenance: number;
    questions_measured: number;
    by_category: Array<{ category: string; count: number }>;
  };
  observation_states: {
    verified_observation: number;
    pending_verification: number;
    not_collected: number;
    failed_collection: number;
    demo_observation: number;
  };
  search_visibility: {
    google_records: number;
    google_ranked_count: number;
    answer_box_observations: number;
    ai_overview_observations: number;
    ai_overview_citing_incubrix: number;
  };
  ai_visibility: {
    total_ai_observations: number;
    incubrix_mentions: number;
    incubrix_citations: number;
    mention_rate_pct: number;
    citation_rate_pct: number;
    by_provider: Array<{
      provider: string;
      total_obs: number;
      verified_obs: number;
      pending_obs: number;
      mentions: number;
      citations: number;
    }>;
    by_market: Array<{
      market: string;
      total_obs: number;
      measured_obs: number;
      mentions: number;
      citations: number;
    }>;
  };
  competitor_mentions: Array<{ competitor: string; mentions: number }>;
  technical_audit: {
    pages_crawled: number;
    issues_total: number;
    by_severity: { critical: number; high: number; medium: number; low: number };
    fixes_validated_patch_tests: number;
    live_site_deployed_fixes: number;
  };
  content_studio: {
    pages_total: number;
    by_status: { ready_to_publish: number; reviewed: number; draft: number };
  };
  citations: {
    opportunities_total: number;
    verified_live: number;
    by_source_type: Array<{ source_type: string; count: number }>;
  };
  two_day_comparison: {
    date_a: string;
    date_b: string;
    paired_count: number;
    two_day_complete: boolean;
    gained_mentions: number;
    gained_citations: number;
    rank_improvements: number;
  };
  latest_run: {
    run_id: string;
    run_type: string;
    mode: string;
    status: string;
    duration_ms: number;
    estimated_cost_usd: number;
    started_at: string;
    completed_at: string;
  } | null;
  computed_at: string;
}
