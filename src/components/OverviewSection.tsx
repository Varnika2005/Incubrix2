import React from 'react';
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  Legend,
  Cell,
} from 'recharts';
import {
  CheckCircle2,
  Clock,
  AlertTriangle,
  XCircle,
  FlaskConical,
  Search,
  Bot,
  ShieldAlert,
  FileText,
  ExternalLink,
  Activity,
  ArrowRight,
  Award,
  Globe,
} from 'lucide-react';
import { OverviewMetrics, SectionId } from '../types';

interface Props {
  metrics: OverviewMetrics | null;
  loading: boolean;
  onNavigate: (section: SectionId) => void;
  onRefresh: () => void;
}

const PROVIDER_LABELS: Record<string, string> = {
  google_search: 'Google SERP/AIO',
  chatgpt: 'ChatGPT',
  gemini: 'Google Gemini',
  perplexity: 'Perplexity Sonar',
  claude: 'Anthropic Claude',
};

export const OverviewSection: React.FC<Props> = ({ metrics, loading, onNavigate, onRefresh }) => {
  if (loading || !metrics) {
    return (
      <div className="p-8 bg-white rounded-xl border border-slate-200 shadow-xs animate-pulse space-y-4">
        <div className="h-6 w-64 bg-slate-200 rounded" />
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
          {[1, 2, 3, 4].map((n) => (
            <div key={n} className="h-28 bg-slate-100 rounded-lg" />
          ))}
        </div>
      </div>
    );
  }

  const providerChartData = metrics.ai_visibility.by_provider.map((p) => ({
    name: PROVIDER_LABELS[p.provider] || p.provider,
    Mentions: p.mentions,
    Citations: p.citations,
    Verified: p.verified_obs,
  }));

  const competitorChartData = metrics.competitor_mentions.slice(0, 8);

  return (
    <div className="space-y-6" data-testid="overview-section">
      {/* Top Evidence Integrity Banner */}
      <div className="bg-gradient-to-r from-cyan-50 via-blue-50 to-indigo-50 border border-cyan-200/80 rounded-xl p-4 flex flex-col md:flex-row items-start md:items-center justify-between gap-4">
        <div className="flex items-start gap-3">
          <div className="p-2 rounded-lg bg-cyan-600 text-white shrink-0 mt-0.5">
            <Activity className="w-5 h-5" />
          </div>
          <div>
            <div className="flex items-center gap-2 flex-wrap">
              <h2 className="text-sm font-bold text-slate-900">
                Evidence-Backed AEO · SEO · GEO Measurement Engine
              </h2>
              <span className="inline-flex items-center px-2 py-0.5 rounded-full text-xs font-semibold bg-emerald-100 text-emerald-800 border border-emerald-300">
                DEMO Records Strictly Excluded from Totals
              </span>
            </div>
            <p className="text-xs text-slate-600 mt-1">
              Target Website:{' '}
              <a
                href="https://www.incubrix.com"
                target="_blank"
                rel="noreferrer"
                className="font-mono font-medium text-cyan-700 underline hover:text-cyan-900"
              >
                https://www.incubrix.com
              </a>{' '}
              (Canonical: <code className="text-slate-800">https://incubrix.com/</code>) · Markets Tracked:{' '}
              <strong>US (en-US)</strong>, <strong>India (en-IN)</strong>, <strong>UK (en-GB)</strong>.
            </p>
          </div>
        </div>
        <div className="flex items-center gap-2 shrink-0">
          <button
            onClick={onRefresh}
            className="px-3 py-1.5 text-xs font-semibold bg-white text-slate-700 border border-slate-300 rounded-lg hover:bg-slate-50 transition cursor-pointer"
          >
            Refresh Computed State
          </button>
          <a
            href="/api/exports/visibility.csv"
            className="px-3 py-1.5 text-xs font-semibold bg-cyan-600 text-white rounded-lg hover:bg-cyan-700 transition inline-flex items-center gap-1.5"
          >
            Export Visibility CSV
          </a>
        </div>
      </div>

      {/* 5 Observation States Strip (Required Provenance & Honesty Breakdown) */}
      <div className="bg-white rounded-xl border border-slate-200 p-4 shadow-2xs">
        <div className="flex items-center justify-between mb-3">
          <h3 className="text-xs font-bold uppercase tracking-wider text-slate-500">
            Observation Collection States (Stored SQLite Records)
          </h3>
          <span className="text-xs text-slate-500">
            AI answers require &ge;2 passes before marking <code className="text-emerald-700 font-semibold">Verified</code>
          </span>
        </div>
        <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-5 gap-3">
          <div className="p-3 rounded-lg bg-emerald-50/70 border border-emerald-200 flex items-center justify-between">
            <div>
              <p className="text-xs font-medium text-emerald-800">Verified Observation</p>
              <p className="text-xl font-bold font-mono text-emerald-950 mt-0.5" data-testid="state-verified">
                {metrics.observation_states.verified_observation}
              </p>
              <p className="text-[11px] text-emerald-700">2-Pass AI / Live SERP</p>
            </div>
            <CheckCircle2 className="w-6 h-6 text-emerald-600 shrink-0" />
          </div>

          <div className="p-3 rounded-lg bg-amber-50/70 border border-amber-200 flex items-center justify-between">
            <div>
              <p className="text-xs font-medium text-amber-800">Pending Verification</p>
              <p className="text-xl font-bold font-mono text-amber-950 mt-0.5" data-testid="state-pending">
                {metrics.observation_states.pending_verification}
              </p>
              <p className="text-[11px] text-amber-700">Single-Pass (Needs Pass 2)</p>
            </div>
            <Clock className="w-6 h-6 text-amber-600 shrink-0" />
          </div>

          <div className="p-3 rounded-lg bg-slate-50 border border-slate-200 flex items-center justify-between">
            <div>
              <p className="text-xs font-medium text-slate-700">Not Collected</p>
              <p className="text-xl font-bold font-mono text-slate-900 mt-0.5" data-testid="state-not-collected">
                {metrics.observation_states.not_collected}
              </p>
              <p className="text-[11px] text-slate-500">Awaiting Ingestion</p>
            </div>
            <AlertTriangle className="w-6 h-6 text-slate-400 shrink-0" />
          </div>

          <div className="p-3 rounded-lg bg-rose-50/70 border border-rose-200 flex items-center justify-between">
            <div>
              <p className="text-xs font-medium text-rose-800">Failed Collection</p>
              <p className="text-xl font-bold font-mono text-rose-950 mt-0.5" data-testid="state-failed">
                {metrics.observation_states.failed_collection}
              </p>
              <p className="text-[11px] text-rose-700">Timeout / HTTP 429</p>
            </div>
            <XCircle className="w-6 h-6 text-rose-500 shrink-0" />
          </div>

          <div className="p-3 rounded-lg bg-violet-50/70 border border-violet-200 flex items-center justify-between">
            <div>
              <div className="flex items-center gap-1.5">
                <p className="text-xs font-medium text-violet-900">Demo Sandbox</p>
                <span className="px-1.5 py-0.2 text-[10px] font-bold bg-violet-200 text-violet-900 rounded">
                  DEMO
                </span>
              </div>
              <p className="text-xl font-bold font-mono text-violet-950 mt-0.5" data-testid="state-demo">
                {metrics.observation_states.demo_observation}
              </p>
              <p className="text-[11px] text-violet-700">Excluded from Totals</p>
            </div>
            <FlaskConical className="w-6 h-6 text-violet-600 shrink-0" />
          </div>
        </div>
      </div>

      {/* Primary KPI Grid (8 Core Project Metrics) */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        {/* Card 1: Questions Collected & Validated */}
        <div className="bg-white rounded-xl border border-slate-200 p-4 shadow-2xs flex flex-col justify-between">
          <div>
            <div className="flex items-center justify-between text-xs font-semibold text-slate-500">
              <span>CREATOR QUESTIONS</span>
              <Search className="w-4 h-4 text-cyan-600" />
            </div>
            <div className="mt-2 flex items-baseline gap-2">
              <span className="text-2xl font-extrabold font-mono text-slate-900" data-testid="kpi-questions-validated">
                {metrics.questions.validated_total}
              </span>
              <span className="text-xs text-emerald-700 font-semibold">
                / {metrics.questions.collected_total} Validated
              </span>
            </div>
            <p className="text-xs text-slate-600 mt-1">
              <strong>{metrics.questions.questions_measured}</strong> questions measured ·{' '}
              <strong>{metrics.questions.duplicates_merged_with_provenance}</strong> duplicates merged keeping provenance
            </p>
          </div>
          <button
            onClick={() => onNavigate('questions')}
            className="mt-3 text-xs font-semibold text-cyan-700 hover:text-cyan-900 inline-flex items-center gap-1 cursor-pointer"
          >
            Inspect 100 Creator Questions <ArrowRight className="w-3.5 h-3.5" />
          </button>
        </div>

        {/* Card 2: Google Visibility & AI Overviews */}
        <div className="bg-white rounded-xl border border-slate-200 p-4 shadow-2xs flex flex-col justify-between">
          <div>
            <div className="flex items-center justify-between text-xs font-semibold text-slate-500">
              <span>GOOGLE SERP & AI OVERVIEWS</span>
              <Globe className="w-4 h-4 text-blue-600" />
            </div>
            <div className="mt-2 flex items-baseline gap-2">
              <span className="text-2xl font-extrabold font-mono text-slate-900">
                {metrics.search_visibility.google_records}
              </span>
              <span className="text-xs text-blue-700 font-semibold">
                SERP Records ({metrics.search_visibility.google_ranked_count} Ranked)
              </span>
            </div>
            <p className="text-xs text-slate-600 mt-1">
              Answer Boxes: <strong>{metrics.search_visibility.answer_box_observations}</strong> · AI Overviews:{' '}
              <strong>{metrics.search_visibility.ai_overview_observations}</strong> (
              <strong>{metrics.search_visibility.ai_overview_citing_incubrix}</strong> citing IncuBrix)
            </p>
          </div>
          <button
            onClick={() => onNavigate('visibility')}
            className="mt-3 text-xs font-semibold text-blue-700 hover:text-blue-900 inline-flex items-center gap-1 cursor-pointer"
          >
            View SERP & Multi-Date Deltas <ArrowRight className="w-3.5 h-3.5" />
          </button>
        </div>

        {/* Card 3: AI Assistant Mention & Citation Rates */}
        <div className="bg-white rounded-xl border border-slate-200 p-4 shadow-2xs flex flex-col justify-between">
          <div>
            <div className="flex items-center justify-between text-xs font-semibold text-slate-500">
              <span>AI ASSISTANT VISIBILITY (AEO/GEO)</span>
              <Bot className="w-4 h-4 text-violet-600" />
            </div>
            <div className="mt-2 flex items-baseline gap-3">
              <div>
                <span className="text-2xl font-extrabold font-mono text-slate-900">
                  {metrics.ai_visibility.mention_rate_pct}%
                </span>
                <span className="text-[11px] text-slate-500 block">Mention Rate</span>
              </div>
              <div className="h-6 w-px bg-slate-200" />
              <div>
                <span className="text-2xl font-extrabold font-mono text-violet-700">
                  {metrics.ai_visibility.citation_rate_pct}%
                </span>
                <span className="text-[11px] text-slate-500 block">Citation Rate</span>
              </div>
            </div>
            <p className="text-xs text-slate-600 mt-1">
              From <strong>{metrics.ai_visibility.total_ai_observations}</strong> measured AI responses across ChatGPT, Gemini, Perplexity & Claude
            </p>
          </div>
          <button
            onClick={() => onNavigate('visibility')}
            className="mt-3 text-xs font-semibold text-violet-700 hover:text-violet-900 inline-flex items-center gap-1 cursor-pointer"
          >
            Open AI Visibility Tracker <ArrowRight className="w-3.5 h-3.5" />
          </button>
        </div>

        {/* Card 4: Technical SEO Audit & Fixes Validated */}
        <div className="bg-white rounded-xl border border-slate-200 p-4 shadow-2xs flex flex-col justify-between">
          <div>
            <div className="flex items-center justify-between text-xs font-semibold text-slate-500">
              <span>TECHNICAL AUDIT (INCUBRIX.COM)</span>
              <ShieldAlert className="w-4 h-4 text-amber-600" />
            </div>
            <div className="mt-2 flex items-baseline gap-2">
              <span className="text-2xl font-extrabold font-mono text-slate-900" data-testid="kpi-issues-total">
                {metrics.technical_audit.issues_total}
              </span>
              <span className="text-xs text-emerald-700 font-semibold">
                ({(metrics.technical_audit as any).live_site_deployed_fixes ?? 0} Live · {metrics.technical_audit.fixes_validated_patch_tests} Patch Tests Validated)
              </span>
            </div>
            <p className="text-xs text-slate-600 mt-1">
              <span className="text-rose-700 font-semibold">{metrics.technical_audit.by_severity.critical} Critical</span> ·{' '}
              <span className="text-amber-700 font-semibold">{metrics.technical_audit.by_severity.high} High</span> ·{' '}
              <span className="text-blue-700 font-semibold">{metrics.technical_audit.by_severity.medium} Med</span> ·{' '}
              <span className="text-slate-600">{metrics.technical_audit.by_severity.low} Low</span> ({metrics.technical_audit.pages_crawled} pages crawled)
            </p>
          </div>
          <button
            onClick={() => onNavigate('audit')}
            className="mt-3 text-xs font-semibold text-amber-700 hover:text-amber-900 inline-flex items-center gap-1 cursor-pointer"
          >
            Inspect 22 Fixes & JSON-LD <ArrowRight className="w-3.5 h-3.5" />
          </button>
        </div>
      </div>

      {/* Secondary Row: Content Studio, Citation Research, Two-Day Delta & Latest Engine Run */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="bg-white rounded-xl border border-slate-200 p-4 shadow-2xs">
          <div className="flex items-center justify-between">
            <span className="text-xs font-bold uppercase tracking-wider text-slate-500">Content Studio Pipeline</span>
            <FileText className="w-4 h-4 text-cyan-600" />
          </div>
          <div className="mt-2 flex items-baseline gap-2">
            <span className="text-2xl font-extrabold font-mono text-slate-900" data-testid="kpi-content-pages">
              {metrics.content_studio.pages_total}
            </span>
            <span className="text-xs text-slate-600">
              Total Pages ({metrics.content_studio.by_status.ready_to_publish} Publish-Ready)
            </span>
          </div>
          <div className="mt-2 flex items-center gap-2 text-xs">
            <span className="px-2 py-0.5 rounded bg-emerald-100 text-emerald-800 font-medium">
              {metrics.content_studio.by_status.ready_to_publish} Ready
            </span>
            <span className="px-2 py-0.5 rounded bg-blue-100 text-blue-800 font-medium">
              {metrics.content_studio.by_status.reviewed} Reviewed
            </span>
            <span className="px-2 py-0.5 rounded bg-slate-100 text-slate-700 font-medium">
              {metrics.content_studio.by_status.draft} Draft
            </span>
          </div>
          <button
            onClick={() => onNavigate('content')}
            className="mt-3 text-xs font-semibold text-cyan-700 hover:underline inline-flex items-center gap-1 cursor-pointer"
          >
            Open Content Studio & Brief Generator <ArrowRight className="w-3.5 h-3.5" />
          </button>
        </div>

        <div className="bg-white rounded-xl border border-slate-200 p-4 shadow-2xs">
          <div className="flex items-center justify-between">
            <span className="text-xs font-bold uppercase tracking-wider text-slate-500">
              Third-Party Citation Targets
            </span>
            <Award className="w-4 h-4 text-indigo-600" />
          </div>
          <div className="mt-2 flex items-baseline gap-2">
            <span className="text-2xl font-extrabold font-mono text-slate-900" data-testid="kpi-citations-total">
              {metrics.citations.opportunities_total}
            </span>
            <span className="text-xs text-emerald-700 font-semibold">
              ({metrics.citations.verified_live} Verified Live URLs)
            </span>
          </div>
          <p className="text-xs text-slate-600 mt-2">
            Directories, comparison roundups, editorial guides & Reddit/IH community threads researched.
          </p>
          <button
            onClick={() => onNavigate('citations')}
            className="mt-3 text-xs font-semibold text-indigo-700 hover:underline inline-flex items-center gap-1 cursor-pointer"
          >
            Explore 30 Citation Opportunities <ArrowRight className="w-3.5 h-3.5" />
          </button>
        </div>

        <div className="bg-white rounded-xl border border-slate-200 p-4 shadow-2xs">
          <div className="flex items-center justify-between">
            <span className="text-xs font-bold uppercase tracking-wider text-slate-500">
              Latest Engine Run & Telemetry
            </span>
            <Activity className="w-4 h-4 text-emerald-600" />
          </div>
          {metrics.latest_run ? (
            <div className="mt-2 space-y-1">
              <div className="flex items-center justify-between">
                <span className="font-mono text-xs font-bold text-slate-900">{metrics.latest_run.run_id}</span>
                <span className="px-2 py-0.5 rounded-full text-[11px] font-semibold bg-emerald-100 text-emerald-800">
                  {metrics.latest_run.status}
                </span>
              </div>
              <p className="text-xs text-slate-600">
                Type: <code className="text-slate-800">{metrics.latest_run.run_type}</code> · Mode:{' '}
                <code className="text-slate-800">{metrics.latest_run.mode}</code>
              </p>
              <p className="text-xs text-slate-600">
                Duration: <strong className="font-mono">{metrics.latest_run.duration_ms} ms</strong> · Est. Cost:{' '}
                <strong className="font-mono">${metrics.latest_run.estimated_cost_usd.toFixed(4)}</strong>
              </p>
              <p className="text-[11px] text-slate-400">
                Two-Day Measurement ({metrics.two_day_comparison.date_a} vs {metrics.two_day_comparison.date_b}):{' '}
                <strong className="text-slate-700">{metrics.two_day_comparison.paired_count} verified pairs</strong>
              </p>
            </div>
          ) : (
            <p className="text-xs text-slate-500 mt-2">No runs recorded yet.</p>
          )}
        </div>
      </div>

      {/* Charts Row: Competitor Mentions vs AI Provider Breakdown */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Competitor Share of Voice */}
        <div className="bg-white rounded-xl border border-slate-200 p-5 shadow-2xs">
          <div className="flex items-center justify-between mb-4">
            <div>
              <h3 className="text-sm font-bold text-slate-900">
                Competitor Mentions in Measured Search & AI Responses
              </h3>
              <p className="text-xs text-slate-500">
                Extracted from non-demo verified and pending observations across US, IN, and GB
              </p>
            </div>
          </div>
          <div className="h-64 w-full">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={competitorChartData} layout="vertical" margin={{ left: 20, right: 20 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="#E2E8F0" />
                <XAxis type="number" tick={{ fontSize: 11, fill: '#475569' }} />
                <YAxis
                  type="category"
                  dataKey="competitor"
                  width={95}
                  tick={{ fontSize: 11, fill: '#0F172A', fontWeight: 600 }}
                />
                <Tooltip
                  contentStyle={{
                    backgroundColor: '#FFFFFF',
                    borderColor: '#CBD5E1',
                    borderRadius: '8px',
                    fontSize: '12px',
                  }}
                />
                <Bar dataKey="mentions" name="Observed Mentions" radius={[0, 6, 6, 0]}>
                  {competitorChartData.map((_, idx) => (
                    <Cell
                      key={idx}
                      fill={idx === 0 ? '#0891B2' : idx === 1 ? '#2563EB' : idx === 2 ? '#7C3AED' : '#64748B'}
                    />
                  ))}
                </Bar>
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Provider Mentions & Citations */}
        <div className="bg-white rounded-xl border border-slate-200 p-5 shadow-2xs">
          <div className="flex items-center justify-between mb-4">
            <div>
              <h3 className="text-sm font-bold text-slate-900">
                IncuBrix Mentions & Citations by Search / AI Provider
              </h3>
              <p className="text-xs text-slate-500">
                Comparing brand mentions vs direct URL citations (https://incubrix.com/*)
              </p>
            </div>
          </div>
          <div className="h-64 w-full">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={providerChartData} margin={{ top: 10, right: 20, left: 0, bottom: 5 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="#E2E8F0" />
                <XAxis dataKey="name" tick={{ fontSize: 11, fill: '#0F172A' }} />
                <YAxis tick={{ fontSize: 11, fill: '#475569' }} />
                <Tooltip
                  contentStyle={{
                    backgroundColor: '#FFFFFF',
                    borderColor: '#CBD5E1',
                    borderRadius: '8px',
                    fontSize: '12px',
                  }}
                />
                <Legend wrapperStyle={{ fontSize: '12px' }} />
                <Bar dataKey="Mentions" fill="#0891B2" radius={[4, 4, 0, 0]} />
                <Bar dataKey="Citations" fill="#7C3AED" radius={[4, 4, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>
    </div>
  );
};
