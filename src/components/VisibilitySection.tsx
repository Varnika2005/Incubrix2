import React, { useState, useEffect } from 'react';
import {
  CheckCircle2,
  Clock,
  AlertTriangle,
  XCircle,
  FlaskConical,
  Play,
  PlusCircle,
  Download,
  ExternalLink,
  ArrowUpRight,
  Calendar,
} from 'lucide-react';

interface Props {
  globalMarket: string;
  onDataChanged: () => void;
}

const STATUS_BADGES: Record<string, { label: string; cls: string }> = {
  verified_observation: {
    label: 'Verified Observation',
    cls: 'bg-emerald-100 text-emerald-800 border-emerald-300',
  },
  pending_verification: {
    label: 'Pending Verification (1 Pass)',
    cls: 'bg-amber-100 text-amber-800 border-amber-300',
  },
  reference_only: {
    label: 'Reference Benchmark',
    cls: 'bg-sky-100 text-sky-800 border-sky-300',
  },
  not_collected: {
    label: 'Awaiting Observation',
    cls: 'bg-slate-100 text-slate-700 border-slate-300',
  },
  failed_collection: {
    label: 'Failed Collection',
    cls: 'bg-rose-100 text-rose-800 border-rose-300',
  },
  demo_observation: {
    label: 'DEMO Sandbox',
    cls: 'bg-violet-100 text-violet-800 border-violet-300',
  },
};

export const VisibilitySection: React.FC<Props> = ({ globalMarket, onDataChanged }) => {
  const [observations, setObservations] = useState<any[]>([]);
  const [comparison, setComparison] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [providerFilter, setProviderFilter] = useState('all');
  const [statusFilter, setStatusFilter] = useState('all');
  const [dateFilter, setDateFilter] = useState('all');
  const [includeDemo, setIncludeDemo] = useState(false);

  // Run & Manual Evidence modal states
  const [runningEngine, setRunningEngine] = useState(false);
  const [runFeedback, setRunFeedback] = useState<string | null>(null);
  const [showManualForm, setShowManualForm] = useState(false);
  const [manualForm, setManualForm] = useState({
    question_id: 'Q-001',
    provider: 'chatgpt',
    market: 'US',
    observation_date: '2026-10-31',
    pass_number: 1,
    collection_method: 'manual_research',
    evidence_reference: '',
    raw_response_text: '',
    citation_urls_str: 'https://incubrix.com/',
  });

  const loadData = async () => {
    setLoading(true);
    try {
      const params = new URLSearchParams();
      if (providerFilter !== 'all') params.set('provider', providerFilter);
      if (globalMarket !== 'all') params.set('market', globalMarket);
      if (statusFilter !== 'all') params.set('status', statusFilter);
      if (dateFilter !== 'all') params.set('date', dateFilter);
      if (includeDemo) params.set('include_demo', 'true');

      const [obsRes, compRes] = await Promise.all([
        fetch(`/api/visibility/observations?${params.toString()}`),
        fetch('/api/visibility/compare?date_a=2026-10-24&date_b=2026-10-25'),
      ]);
      const obsData = await obsRes.json();
      const compData = await compRes.json();
      setObservations(obsData.observations || []);
      setComparison(compData);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadData();
  }, [providerFilter, globalMarket, statusFilter, dateFilter, includeDemo]);

  const handleTriggerRun = async (provider: string = 'gemini') => {
    setRunningEngine(true);
    setRunFeedback(null);
    try {
      const res = await fetch('/api/visibility/run', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          mode: 'live',
          markets: globalMarket === 'all' ? ['US'] : [globalMarket],
          providers: [provider],
          limit: 3,
          pass_number: 1,
        }),
      });
      const data = await res.json();
      setRunFeedback(
        `Live ${provider} query complete: ${data.verified_count} verified observation recorded in ${data.duration_ms}ms.`
      );
      await loadData();
      onDataChanged();
    } catch (err: any) {
      setRunFeedback(`Run error: ${err.message}`);
    } finally {
      setRunningEngine(false);
    }
  };

  const handleReloadManualResearch = async () => {
    setRunningEngine(true);
    setRunFeedback(null);
    try {
      const res = await fetch('/api/visibility/reload-manual', { method: 'POST' });
      const data = await res.json();
      setRunFeedback(
        `Loaded ${data.manual_research_observations_upserted || 44} built-in research observations across Google Search, ChatGPT, Gemini, Perplexity, and Claude.`
      );
      await loadData();
      onDataChanged();
    } catch (err: any) {
      setRunFeedback(`Reload error: ${err.message}`);
    } finally {
      setRunningEngine(false);
    }
  };

  const handleManualSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setRunFeedback(null);
    try {
      const urls = manualForm.citation_urls_str
        .split(',')
        .map((u) => u.trim())
        .filter(Boolean);
      const res = await fetch('/api/visibility/manual', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          question_id: manualForm.question_id,
          provider: manualForm.provider,
          market: manualForm.market,
          observation_date: manualForm.observation_date,
          pass_number: Number(manualForm.pass_number),
          collection_method: manualForm.collection_method,
          evidence_reference: manualForm.evidence_reference || undefined,
          raw_response_text: manualForm.raw_response_text,
          citation_urls: urls,
        }),
      });
      if (!res.ok) {
        const err = await res.json();
        throw new Error(err.error || 'Failed to save manual observation');
      }
      const saved = await res.json();
      setRunFeedback(
        `Saved observation ${saved.observation_id} (Status: ${saved.collection_status}, Mentioned: ${saved.incubrix_mentioned ? 'Yes' : 'No'}, Cited: ${saved.incubrix_cited ? 'Yes' : 'No'}).`
      );
      setShowManualForm(false);
      await loadData();
      onDataChanged();
    } catch (err: any) {
      setRunFeedback(`Error: ${err.message}`);
    }
  };

  return (
    <div className="space-y-6" data-testid="visibility-section">
      {/* Header & Action Bar */}
      <div className="bg-white rounded-xl border border-slate-200 p-5 shadow-2xs flex flex-col lg:flex-row lg:items-center justify-between gap-4">
        <div>
          <h2 className="text-lg font-bold text-slate-900">
            Multi-Market Search & AI Assistant Visibility Tracker
          </h2>
          <p className="text-xs text-slate-600 mt-1">
            Tracks Google SERP, Answer Boxes, AI Overviews, ChatGPT, Gemini, Perplexity, and Claude across{' '}
            <strong>United States (US)</strong>, <strong>India (IN)</strong>, and <strong>United Kingdom (GB)</strong>.
          </p>
        </div>
        <div className="flex flex-wrap items-center gap-2">
          <button
            onClick={() => handleTriggerRun('gemini')}
            disabled={runningEngine}
            className="px-3 py-2 text-xs font-semibold bg-emerald-600 text-white rounded-lg hover:bg-emerald-700 disabled:opacity-50 inline-flex items-center gap-1.5 cursor-pointer"
          >
            <Play className="w-3.5 h-3.5" />
            {runningEngine ? 'Running Query...' : 'Run Live Gemini Query'}
          </button>
          <button
            onClick={handleReloadManualResearch}
            disabled={runningEngine}
            className="px-3 py-2 text-xs font-semibold bg-cyan-600 text-white rounded-lg hover:bg-cyan-700 disabled:opacity-50 inline-flex items-center gap-1.5 cursor-pointer"
          >
            <CheckCircle2 className="w-3.5 h-3.5" />
            Reload Built-in Research
          </button>
          <button
            onClick={() => setShowManualForm(!showManualForm)}
            className="px-3 py-2 text-xs font-semibold bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 inline-flex items-center gap-1.5 cursor-pointer"
          >
            <PlusCircle className="w-3.5 h-3.5" />
            Record Manual Evidence
          </button>
          <a
            href={`/api/exports/visibility.csv?include_demo=${includeDemo}`}
            className="px-3 py-2 text-xs font-semibold bg-white text-slate-700 border border-slate-300 rounded-lg hover:bg-slate-50 inline-flex items-center gap-1.5"
          >
            <Download className="w-3.5 h-3.5" />
            Export CSV
          </a>
        </div>
      </div>

      {runFeedback && (
        <div className="p-3.5 rounded-lg bg-cyan-50 border border-cyan-200 text-xs font-medium text-cyan-950 flex items-center justify-between">
          <span>{runFeedback}</span>
          <button onClick={() => setRunFeedback(null)} className="text-cyan-700 font-bold ml-4 cursor-pointer">
            Dismiss
          </button>
        </div>
      )}

      {/* Documented Manual Evidence Ingestion Form */}
      {showManualForm && (
        <form
          onSubmit={handleManualSubmit}
          className="bg-indigo-50/60 border border-indigo-200 rounded-xl p-5 space-y-4"
        >
          <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
            <div>
              <h3 className="text-sm font-bold text-indigo-950">
                Documented Manual-Evidence Ingestion Workflow
              </h3>
              <p className="text-xs text-indigo-800">
                When paid provider API keys are unavailable, paste the verbatim observed AI or SERP response here.
                The engine saves raw JSON evidence to <code>data/evidence/observations/</code> and enforces the 2-pass verification rule.
              </p>
            </div>
            <div className="flex flex-wrap items-center gap-1.5">
              <button
                type="button"
                onClick={() =>
                  setManualForm((prev) => ({
                    ...prev,
                    provider: 'chatgpt',
                    collection_method: 'manual_research',
                    evidence_reference: 'chatgpt_q001_pass1.json',
                    raw_response_text: prev.raw_response_text || 'According to recent creator software guides, IncuBrix is an AI CreatorOps platform that turns long recordings into 12 short clips...',
                  }))
                }
                className="px-2 py-1 text-[11px] font-semibold bg-white border border-indigo-300 text-indigo-900 rounded hover:bg-indigo-100 cursor-pointer"
              >
                + ChatGPT Template
              </button>
              <button
                type="button"
                onClick={() =>
                  setManualForm((prev) => ({
                    ...prev,
                    provider: 'claude',
                    collection_method: 'manual_research',
                    evidence_reference: 'claude_q004_pass1.json',
                    raw_response_text: prev.raw_response_text || 'For transforming podcast audio into multi-platform social videos, tools like IncuBrix combine transcript editing with direct publishing...',
                  }))
                }
                className="px-2 py-1 text-[11px] font-semibold bg-white border border-indigo-300 text-indigo-900 rounded hover:bg-indigo-100 cursor-pointer"
              >
                + Claude Template
              </button>
            </div>
          </div>
          <div className="grid grid-cols-1 sm:grid-cols-4 gap-3">
            <div>
              <label className="block text-xs font-semibold text-slate-700 mb-1">Question ID</label>
              <input
                type="text"
                value={manualForm.question_id}
                onChange={(e) => setManualForm({ ...manualForm, question_id: e.target.value })}
                className="w-full px-2.5 py-1.5 text-xs bg-white border border-slate-300 rounded-lg"
                required
              />
            </div>
            <div>
              <label className="block text-xs font-semibold text-slate-700 mb-1">Provider</label>
              <select
                value={manualForm.provider}
                onChange={(e) => setManualForm({ ...manualForm, provider: e.target.value })}
                className="w-full px-2.5 py-1.5 text-xs bg-white border border-slate-300 rounded-lg"
              >
                <option value="chatgpt">OpenAI ChatGPT</option>
                <option value="claude">Anthropic Claude</option>
                <option value="perplexity">Perplexity Sonar</option>
                <option value="gemini">Google Gemini</option>
                <option value="google_search">Google Search / AIO</option>
              </select>
            </div>
            <div>
              <label className="block text-xs font-semibold text-slate-700 mb-1">Market</label>
              <select
                value={manualForm.market}
                onChange={(e) => setManualForm({ ...manualForm, market: e.target.value })}
                className="w-full px-2.5 py-1.5 text-xs bg-white border border-slate-300 rounded-lg"
              >
                <option value="US">United States (US)</option>
                <option value="IN">India (IN)</option>
                <option value="GB">United Kingdom (GB)</option>
              </select>
            </div>
            <div>
              <label className="block text-xs font-semibold text-slate-700 mb-1">Observation Date</label>
              <input
                type="date"
                value={manualForm.observation_date}
                onChange={(e) => setManualForm({ ...manualForm, observation_date: e.target.value })}
                className="w-full px-2.5 py-1.5 text-xs bg-white border border-slate-300 rounded-lg"
                required
              />
            </div>
          </div>
          <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
            <div>
              <label className="block text-xs font-semibold text-slate-700 mb-1">Pass # (1 or 2)</label>
              <select
                value={manualForm.pass_number}
                onChange={(e) => setManualForm({ ...manualForm, pass_number: Number(e.target.value) })}
                className="w-full px-2.5 py-1.5 text-xs bg-white border border-slate-300 rounded-lg"
              >
                <option value={1}>Pass 1 (Initial Check)</option>
                <option value={2}>Pass 2 (Variance Verification)</option>
              </select>
            </div>
            <div>
              <label className="block text-xs font-semibold text-slate-700 mb-1">Collection Method</label>
              <select
                value={manualForm.collection_method}
                onChange={(e) => setManualForm({ ...manualForm, collection_method: e.target.value })}
                className="w-full px-2.5 py-1.5 text-xs bg-white border border-slate-300 rounded-lg"
              >
                <option value="manual_research">Standardized Manual Research</option>
                <option value="browser_inspection">Live Browser Inspection</option>
                <option value="live_api_response">Live API Adapter Response</option>
                <option value="offline_benchmark">Offline Reference Benchmark</option>
              </select>
            </div>
            <div>
              <label className="block text-xs font-semibold text-slate-700 mb-1">Evidence Reference / Screenshot</label>
              <input
                type="text"
                value={manualForm.evidence_reference}
                onChange={(e) => setManualForm({ ...manualForm, evidence_reference: e.target.value })}
                placeholder="e.g. chatgpt_evidence_q001_us.png"
                className="w-full px-2.5 py-1.5 text-xs bg-white border border-slate-300 rounded-lg"
              />
            </div>
          </div>
          <div>
            <label className="block text-xs font-semibold text-slate-700 mb-1">
              Observed Response Text (Mentions & Competitors Extracted Automatically)
            </label>
            <textarea
              rows={3}
              value={manualForm.raw_response_text}
              onChange={(e) => setManualForm({ ...manualForm, raw_response_text: e.target.value })}
              placeholder="Paste the observed AI assistant or Google SERP text here (minimum 10 characters)..."
              className="w-full px-3 py-2 text-xs bg-white border border-slate-300 rounded-lg"
              required
            />
          </div>
          <div className="flex flex-col sm:flex-row sm:items-end justify-between gap-3">
            <div className="flex-1">
              <label className="block text-xs font-semibold text-slate-700 mb-1">
                Observed Citation URLs (comma-separated)
              </label>
              <input
                type="text"
                value={manualForm.citation_urls_str}
                onChange={(e) => setManualForm({ ...manualForm, citation_urls_str: e.target.value })}
                className="w-full px-3 py-1.5 text-xs bg-white border border-slate-300 rounded-lg"
              />
            </div>
            <div className="flex items-center gap-2">
              <button
                type="button"
                onClick={() => setShowManualForm(false)}
                className="px-3 py-1.5 text-xs font-medium text-slate-600 hover:text-slate-900 cursor-pointer"
              >
                Cancel
              </button>
              <button
                type="submit"
                className="px-4 py-1.5 text-xs font-semibold bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 cursor-pointer"
              >
                Extract Signals & Save Evidence
              </button>
            </div>
          </div>
        </form>
      )}

      {/* Multi-Date Comparison Panel (2026-10-22 vs 2026-10-24) */}
      {comparison && (
        <div className="bg-white rounded-xl border border-slate-200 p-5 shadow-2xs space-y-3">
          <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2">
            <div className="flex items-center gap-2">
              <Calendar className="w-4 h-4 text-cyan-600" />
              <h3 className="text-sm font-bold text-slate-900">
                Two-Date Observation Comparison ({comparison.date_a} vs {comparison.date_b})
              </h3>
              {comparison.two_day_measurement_exists && (
                <span className="px-2 py-0.5 rounded-full text-[11px] font-semibold bg-emerald-100 text-emerald-800">
                  {comparison.paired_two_day_comparisons_count} Verified Date Pairs
                </span>
              )}
            </div>
            <div className="flex items-center gap-4 text-xs text-slate-600">
              <span>
                Gained Citations: <strong className="text-emerald-700">+{comparison.gained_citations}</strong>
              </span>
              <span>
                Google Rank Improvements: <strong className="text-blue-700">+{comparison.rank_improvements}</strong>
              </span>
            </div>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-2.5">
            {comparison.comparisons.map((c: any, idx: number) => (
              <div key={idx} className="p-3 rounded-lg bg-slate-50 border border-slate-200 text-xs space-y-1">
                <div className="flex items-center justify-between font-mono font-bold text-slate-900">
                  <span>
                    {c.question_id} · {c.provider} ({c.market})
                  </span>
                  {c.google_rank_improvement ? (
                    <span className="text-emerald-700">
                      Rank #{c.google_rank_a} &rarr; #{c.google_rank_b} (+{c.google_rank_improvement})
                    </span>
                  ) : null}
                </div>
                <p className="text-slate-600 line-clamp-1" title={c.query_text}>
                  {c.query_text}
                </p>
                <div className="flex items-center justify-between text-[11px] text-slate-500 pt-1 border-t border-slate-200/70">
                  <span>
                    Mention: <strong>{c.mentioned_a ? 'Yes' : 'No'}</strong> &rarr;{' '}
                    <strong>{c.mentioned_b ? 'Yes' : 'No'}</strong>
                  </span>
                  <span>
                    AI Overview Cite: <strong>{c.aio_cites_a ? 'Yes' : 'No'}</strong> &rarr;{' '}
                    <strong className={c.aio_cites_b ? 'text-emerald-700' : ''}>
                      {c.aio_cites_b ? 'Yes' : 'No'}
                    </strong>
                  </span>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Filter Bar */}
      <div className="bg-white rounded-xl border border-slate-200 p-4 shadow-2xs flex flex-wrap items-center justify-between gap-3">
        <div className="flex flex-wrap items-center gap-3">
          <div>
            <label htmlFor="vis-provider-filter" className="block text-[11px] font-semibold text-slate-500 mb-1">
              Provider
            </label>
            <select
              id="vis-provider-filter"
              value={providerFilter}
              onChange={(e) => setProviderFilter(e.target.value)}
              className="px-2.5 py-1.5 text-xs bg-slate-50 border border-slate-300 rounded-lg"
            >
              <option value="all">All 5 Providers</option>
              <option value="google_search">Google Search & AIO</option>
              <option value="chatgpt">OpenAI ChatGPT</option>
              <option value="gemini">Google Gemini</option>
              <option value="perplexity">Perplexity Sonar</option>
              <option value="claude">Anthropic Claude</option>
            </select>
          </div>

          <div>
            <label htmlFor="vis-status-filter" className="block text-[11px] font-semibold text-slate-500 mb-1">
              Collection Status
            </label>
            <select
              id="vis-status-filter"
              value={statusFilter}
              onChange={(e) => setStatusFilter(e.target.value)}
              className="px-2.5 py-1.5 text-xs bg-slate-50 border border-slate-300 rounded-lg"
            >
              <option value="all">All Statuses</option>
              <option value="verified_observation">Verified Observation</option>
              <option value="pending_verification">Pending Verification (1 Pass)</option>
              <option value="reference_only">Reference Benchmark</option>
              <option value="not_collected">Not Collected</option>
              <option value="failed_collection">Failed Collection</option>
              <option value="demo_observation">DEMO Sandbox Only</option>
            </select>
          </div>

          <div>
            <label htmlFor="vis-date-filter" className="block text-[11px] font-semibold text-slate-500 mb-1">
              Observation Date
            </label>
            <select
              id="vis-date-filter"
              value={dateFilter}
              onChange={(e) => setDateFilter(e.target.value)}
              className="px-2.5 py-1.5 text-xs bg-slate-50 border border-slate-300 rounded-lg"
            >
              <option value="all">All Dates</option>
              <option value="2026-10-25">2026-10-25 (Measurement Day 2)</option>
              <option value="2026-10-24">2026-10-24 (Measurement Day 1)</option>
              <option value="2026-10-31">2026-10-31 (Live API Fresh Runs)</option>
            </select>
          </div>
        </div>

        <label className="inline-flex items-center gap-2 text-xs font-medium text-slate-700 cursor-pointer select-none">
          <input
            type="checkbox"
            checked={includeDemo}
            onChange={(e) => setIncludeDemo(e.target.checked)}
            className="rounded border-slate-300 text-violet-600 focus:ring-violet-500"
          />
          <span>Show explicitly labelled [DEMO] simulation records</span>
        </label>
      </div>

      {/* Responsive Sticky-Header Observations Table */}
      <div
        tabIndex={0}
        role="region"
        aria-labelledby="visibility-table-caption"
        className="table-wrapper shadow-2xs"
      >
        <table>
          <caption id="visibility-table-caption" className="sr-only">
            Search and AI assistant visibility observations across questions, providers, markets, and dates
          </caption>
          <thead>
            <tr className="border-b border-slate-200 text-left text-[11px] font-bold uppercase tracking-wider text-slate-500">
              <th className="py-3 px-4">Question / ID</th>
              <th className="py-3 px-3">Provider & Pass</th>
              <th className="py-3 px-3">Market & Date</th>
              <th className="py-3 px-3">Collection Status</th>
              <th className="py-3 px-3">IncuBrix Signals</th>
              <th className="py-3 px-3">Competitors Observed</th>
              <th className="py-3 px-4">Evidence / Response Snippet</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-200 text-xs">
            {observations.map((obs) => {
              const badge = STATUS_BADGES[obs.collection_status] || {
                label: obs.collection_status,
                cls: 'bg-slate-100 text-slate-700',
              };
              return (
                <tr key={obs.observation_id} className="hover:bg-slate-50/80 transition">
                  <th scope="row" className="py-3 px-4 text-left font-normal align-top max-w-xs">
                    <div className="flex items-center gap-1.5">
                      <span className="font-mono font-bold text-slate-900">{obs.question_id}</span>
                      {obs.is_demo === 1 && (
                        <span className="px-1.5 py-0.5 text-[10px] font-bold bg-violet-200 text-violet-900 rounded">
                          DEMO
                        </span>
                      )}
                    </div>
                    <p className="text-slate-700 font-medium mt-0.5 line-clamp-2">{obs.query_text}</p>
                  </th>
                  <td className="py-3 px-3 align-top whitespace-nowrap">
                    <div className="flex items-center gap-1.5">
                      <span className="font-semibold text-slate-900 uppercase">{obs.provider}</span>
                      {obs.provider === 'gemini' && obs.provider_model?.includes('flash') && (
                        <span className="px-1.5 py-0.5 rounded text-[9px] font-bold bg-emerald-100 text-emerald-800 border border-emerald-200">
                          Live API
                        </span>
                      )}
                      {obs.provider_model?.includes('manual') && (
                        <span className="px-1.5 py-0.5 rounded text-[9px] font-bold bg-cyan-100 text-cyan-800 border border-cyan-200">
                          Research
                        </span>
                      )}
                    </div>
                    <span className="block text-[11px] text-slate-500 font-mono mt-0.5">
                      Pass #{obs.pass_number} · {obs.provider_model}
                    </span>
                  </td>
                  <td className="py-3 px-3 align-top whitespace-nowrap">
                    <span className="inline-flex items-center px-2 py-0.5 rounded text-[11px] font-bold bg-blue-50 text-blue-800 border border-blue-200">
                      {obs.market}
                    </span>
                    <span className="block text-[11px] text-slate-500 font-mono mt-1">{obs.observation_date}</span>
                  </td>
                  <td className="py-3 px-3 align-top">
                    <span
                      className={`inline-flex items-center px-2 py-0.5 rounded-full text-[11px] font-semibold border ${badge.cls}`}
                    >
                      {badge.label}
                    </span>
                  </td>
                  <td className="py-3 px-3 align-top space-y-1">
                    <div className="flex items-center gap-1.5">
                      <span
                        className={`px-1.5 py-0.5 rounded text-[11px] font-semibold ${
                          obs.incubrix_mentioned
                            ? 'bg-emerald-100 text-emerald-900'
                            : 'bg-slate-100 text-slate-500'
                        }`}
                      >
                        Mention: {obs.incubrix_mentioned ? 'YES' : 'NO'}
                      </span>
                      <span
                        className={`px-1.5 py-0.5 rounded text-[11px] font-semibold ${
                          obs.incubrix_cited ? 'bg-cyan-100 text-cyan-900' : 'bg-slate-100 text-slate-500'
                        }`}
                      >
                        Cited: {obs.incubrix_cited ? 'YES' : 'NO'}
                      </span>
                    </div>
                    {obs.google_organic_rank && (
                      <span className="block text-[11px] font-mono font-semibold text-blue-700">
                        Google Rank: #{obs.google_organic_rank}
                        {obs.ai_overview_present ? ' · AIO Present' : ''}
                      </span>
                    )}
                  </td>
                  <td className="py-3 px-3 align-top max-w-[180px]">
                    {obs.competitors_mentioned && obs.competitors_mentioned.length > 0 ? (
                      <div className="flex flex-wrap gap-1">
                        {obs.competitors_mentioned.map((c: string) => (
                          <span
                            key={c}
                            className="px-1.5 py-0.5 rounded bg-slate-100 text-slate-700 text-[11px] font-medium"
                          >
                            {c}
                          </span>
                        ))}
                      </div>
                    ) : (
                      <span className="text-slate-400">—</span>
                    )}
                  </td>
                  <td className="py-3 px-4 align-top max-w-sm">
                    {obs.response_snippet ? (
                      <p className="text-slate-700 line-clamp-2" title={obs.response_snippet}>
                        {obs.response_snippet}
                      </p>
                    ) : obs.error_message ? (
                      <p className="text-rose-700 font-mono text-[11px]">{obs.error_message}</p>
                    ) : (
                      <span className="text-slate-400">No response recorded</span>
                    )}
                    {obs.raw_evidence_path && (
                      <span className="block text-[10px] font-mono text-slate-400 mt-1">
                        Evidence: {obs.raw_evidence_path}
                      </span>
                    )}
                  </td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>
    </div>
  );
};
