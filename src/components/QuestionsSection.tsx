import React, { useState, useEffect } from 'react';
import { Search, PlusCircle, Download, CheckCircle2, ExternalLink } from 'lucide-react';

interface Props {
  onDataChanged: () => void;
}

export const QuestionsSection: React.FC<Props> = ({ onDataChanged }) => {
  const [questions, setQuestions] = useState<any[]>([]);
  const [tierCounts, setTierCounts] = useState({
    total_prepared: 100,
    genuine_verified: 10,
    partially_measured: 2,
    reference_only: 41,
    awaiting_measurement: 45,
    demo: 2,
  });
  const [categoryFilter, setCategoryFilter] = useState('all');
  const [intentFilter, setIntentFilter] = useState('all');
  const [tierFilter, setTierFilter] = useState('all');
  const [searchTerm, setSearchTerm] = useState('');
  const [showAddForm, setShowAddForm] = useState(false);
  const [feedback, setFeedback] = useState<string | null>(null);

  const [newQ, setNewQ] = useState({
    canonical_question: '',
    original_wording: '',
    category: 'Content Creation',
    search_intent: 'informational',
    target_persona: 'YouTube Creator',
    source_url: 'https://www.reddit.com/r/NewTubers/',
    source_type: 'public_community',
    collection_date: '2026-10-24',
    priority_score: 85,
  });

  const loadQuestions = async () => {
    const params = new URLSearchParams();
    if (categoryFilter !== 'all') params.set('category', categoryFilter);
    if (intentFilter !== 'all') params.set('intent', intentFilter);
    if (tierFilter !== 'all') params.set('evidence_tier', tierFilter);
    if (searchTerm.trim()) params.set('search', searchTerm.trim());

    const res = await fetch(`/api/questions?${params.toString()}`);
    const data = await res.json();
    setQuestions(data.questions || []);
    if (data.tier_counts) {
      setTierCounts(data.tier_counts);
    }
  };

  useEffect(() => {
    loadQuestions();
  }, [categoryFilter, intentFilter, tierFilter, searchTerm]);

  const handleAddQuestion = async (e: React.FormEvent) => {
    e.preventDefault();
    setFeedback(null);
    try {
      const res = await fetch('/api/questions', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(newQ),
      });
      const data = await res.json();
      if (!res.ok) {
        throw new Error(data.error || 'Validation failed');
      }
      setFeedback(
        data.action === 'merged_into_existing_preserving_provenance'
          ? `Deduplicated! Merged new source URL and original wording into existing question ${data.question.id} without destroying provenance.`
          : `Added and validated new question ${data.question.id}.`
      );
      setShowAddForm(false);
      await loadQuestions();
      onDataChanged();
    } catch (err: any) {
      setFeedback(`Error: ${err.message}`);
    }
  };

  return (
    <div className="space-y-6" data-testid="questions-section">
      {/* Header */}
      <div className="bg-white rounded-xl border border-slate-200 p-5 shadow-2xs flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h2 className="text-lg font-bold text-slate-900">
            Creator Research Questions Pipeline ({questions.length} Validated Queries)
          </h2>
          <p className="text-xs text-slate-600 mt-1">
            100 real creator questions across 7 categories with source URL, source type, collection date, original wording,
            and non-destructive fingerprint deduplication.
          </p>
        </div>
        <div className="flex items-center gap-2">
          <button
            onClick={() => setShowAddForm(!showAddForm)}
            className="px-3 py-2 text-xs font-semibold bg-cyan-600 text-white rounded-lg hover:bg-cyan-700 inline-flex items-center gap-1.5 cursor-pointer"
          >
            <PlusCircle className="w-3.5 h-3.5" />
            Add / Deduplicate Question
          </button>
          <a
            href="/api/exports/questions.csv"
            className="px-3 py-2 text-xs font-semibold bg-white text-slate-700 border border-slate-300 rounded-lg hover:bg-slate-50 inline-flex items-center gap-1.5"
          >
            <Download className="w-3.5 h-3.5" />
            Export 100 Questions CSV
          </a>
        </div>
      </div>

      {/* Evidence Tier Summary Stat Cards */}
      <div className="grid grid-cols-2 sm:grid-cols-6 gap-3">
        <div className="bg-white p-3 rounded-xl border border-slate-200 shadow-2xs">
          <div className="text-[11px] font-bold text-slate-500 uppercase tracking-wider">Total Prepared</div>
          <div className="text-xl font-extrabold text-slate-900 mt-0.5">{tierCounts.total_prepared}</div>
          <div className="text-[10px] text-slate-500 mt-0.5">100% deduped</div>
        </div>
        <div className="bg-emerald-50/60 p-3 rounded-xl border border-emerald-200 shadow-2xs">
          <div className="text-[11px] font-bold text-emerald-800 uppercase tracking-wider">Genuine Verified</div>
          <div className="text-xl font-extrabold text-emerald-900 mt-0.5">{tierCounts.genuine_verified}</div>
          <div className="text-[10px] text-emerald-700 mt-0.5">2-Pass verified</div>
        </div>
        <div className="bg-amber-50/60 p-3 rounded-xl border border-amber-200 shadow-2xs">
          <div className="text-[11px] font-bold text-amber-800 uppercase tracking-wider">Partially Measured</div>
          <div className="text-xl font-extrabold text-amber-900 mt-0.5">{tierCounts.partially_measured}</div>
          <div className="text-[10px] text-amber-700 mt-0.5">1-Pass baseline</div>
        </div>
        <div className="bg-sky-50/60 p-3 rounded-xl border border-sky-200 shadow-2xs">
          <div className="text-[11px] font-bold text-sky-800 uppercase tracking-wider">Reference Only</div>
          <div className="text-xl font-extrabold text-sky-900 mt-0.5">{tierCounts.reference_only}</div>
          <div className="text-[10px] text-sky-700 mt-0.5">Studio benchmark</div>
        </div>
        <div className="bg-slate-50 p-3 rounded-xl border border-slate-200 shadow-2xs">
          <div className="text-[11px] font-bold text-slate-600 uppercase tracking-wider">Awaiting Measurement</div>
          <div className="text-xl font-extrabold text-slate-800 mt-0.5">{tierCounts.awaiting_measurement}</div>
          <div className="text-[10px] text-slate-500 mt-0.5">Queued pipeline</div>
        </div>
        <div className="bg-violet-50/60 p-3 rounded-xl border border-violet-200 shadow-2xs">
          <div className="text-[11px] font-bold text-violet-800 uppercase tracking-wider">DEMO Sandbox</div>
          <div className="text-xl font-extrabold text-violet-900 mt-0.5">{tierCounts.demo}</div>
          <div className="text-[10px] text-violet-700 mt-0.5">Simulation only</div>
        </div>
      </div>

      {feedback && (
        <div className="p-3.5 rounded-lg bg-emerald-50 border border-emerald-200 text-xs font-medium text-emerald-950">
          {feedback}
        </div>
      )}

      {/* Add / Deduplicate Question Form */}
      {showAddForm && (
        <form
          onSubmit={handleAddQuestion}
          className="bg-cyan-50/60 border border-cyan-200 rounded-xl p-5 space-y-4 text-xs"
        >
          <h3 className="text-sm font-bold text-cyan-950">
            Import or Test Non-Destructive Question Deduplication
          </h3>
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
            <div>
              <label className="block font-semibold text-slate-700 mb-1">Canonical Question</label>
              <input
                type="text"
                value={newQ.canonical_question}
                onChange={(e) => setNewQ({ ...newQ, canonical_question: e.target.value })}
                placeholder="e.g. What is the best AI studio to turn one recording into a full week of creator content?"
                className="w-full px-3 py-1.5 bg-white border border-slate-300 rounded-lg"
                required
              />
            </div>
            <div>
              <label className="block font-semibold text-slate-700 mb-1">Original Wording (Provenance)</label>
              <input
                type="text"
                value={newQ.original_wording}
                onChange={(e) => setNewQ({ ...newQ, original_wording: e.target.value })}
                placeholder="Verbatim search or forum phrasing..."
                className="w-full px-3 py-1.5 bg-white border border-slate-300 rounded-lg"
                required
              />
            </div>
          </div>
          <div className="grid grid-cols-1 sm:grid-cols-4 gap-3">
            <div>
              <label className="block font-semibold text-slate-700 mb-1">Category</label>
              <select
                value={newQ.category}
                onChange={(e) => setNewQ({ ...newQ, category: e.target.value })}
                className="w-full px-2.5 py-1.5 bg-white border border-slate-300 rounded-lg"
              >
                <option value="Content Creation">Content Creation</option>
                <option value="AI Video Editing">AI Video Editing</option>
                <option value="Content Repurposing">Content Repurposing</option>
                <option value="Captioning & Voiceovers">Captioning & Voiceovers</option>
                <option value="Multi-Platform Publishing">Multi-Platform Publishing</option>
                <option value="Creator Growth & Analytics">Creator Growth & Analytics</option>
                <option value="Product Comparisons">Product Comparisons</option>
              </select>
            </div>
            <div>
              <label className="block font-semibold text-slate-700 mb-1">Source URL</label>
              <input
                type="url"
                value={newQ.source_url}
                onChange={(e) => setNewQ({ ...newQ, source_url: e.target.value })}
                className="w-full px-2.5 py-1.5 bg-white border border-slate-300 rounded-lg"
                required
              />
            </div>
            <div>
              <label className="block font-semibold text-slate-700 mb-1">Source Type</label>
              <select
                value={newQ.source_type}
                onChange={(e) => setNewQ({ ...newQ, source_type: e.target.value })}
                className="w-full px-2.5 py-1.5 bg-white border border-slate-300 rounded-lg"
              >
                <option value="public_community">public_community</option>
                <option value="search_autocomplete_paa">search_autocomplete_paa</option>
                <option value="first_party_faq">first_party_faq</option>
                <option value="industry_directory">industry_directory</option>
                <option value="competitor_docs">competitor_docs</option>
                <option value="editorial_research">editorial_research</option>
              </select>
            </div>
            <div className="flex items-end">
              <button
                type="submit"
                className="w-full px-4 py-1.5 font-semibold bg-cyan-600 text-white rounded-lg hover:bg-cyan-700 cursor-pointer"
              >
                Validate & Save Question
              </button>
            </div>
          </div>
        </form>
      )}

      {/* Filter Bar */}
      <div className="bg-white rounded-xl border border-slate-200 p-4 shadow-2xs flex flex-wrap items-center justify-between gap-3">
        <div className="flex flex-wrap items-center gap-3">
          <div className="relative">
            <Search className="w-3.5 h-3.5 text-slate-400 absolute left-3 top-2.5" />
            <input
              type="text"
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              placeholder="Search 100 questions or IDs..."
              className="pl-8 pr-3 py-1.5 text-xs bg-slate-50 border border-slate-300 rounded-lg w-64"
            />
          </div>

          <select
            aria-label="Filter questions by category"
            value={categoryFilter}
            onChange={(e) => setCategoryFilter(e.target.value)}
            className="px-2.5 py-1.5 text-xs bg-slate-50 border border-slate-300 rounded-lg"
          >
            <option value="all">All 7 Categories</option>
            <option value="Content Creation">Content Creation</option>
            <option value="AI Video Editing">AI Video Editing</option>
            <option value="Content Repurposing">Content Repurposing</option>
            <option value="Captioning & Voiceovers">Captioning & Voiceovers</option>
            <option value="Multi-Platform Publishing">Multi-Platform Publishing</option>
            <option value="Creator Growth & Analytics">Creator Growth & Analytics</option>
            <option value="Product Comparisons">Product Comparisons</option>
          </select>

          <select
            aria-label="Filter questions by intent"
            value={intentFilter}
            onChange={(e) => setIntentFilter(e.target.value)}
            className="px-2.5 py-1.5 text-xs bg-slate-50 border border-slate-300 rounded-lg"
          >
            <option value="all">All Intents</option>
            <option value="informational">Informational</option>
            <option value="commercial">Commercial</option>
            <option value="comparative">Comparative</option>
            <option value="transactional">Transactional</option>
          </select>

          <select
            aria-label="Filter questions by evidence tier"
            value={tierFilter}
            onChange={(e) => setTierFilter(e.target.value)}
            className="px-2.5 py-1.5 text-xs bg-slate-50 border border-slate-300 rounded-lg font-semibold text-slate-700"
          >
            <option value="all">All Evidence Tiers</option>
            <option value="GENUINE_VERIFIED">Genuine Verified ({tierCounts.genuine_verified})</option>
            <option value="PARTIALLY_MEASURED">Partially Measured ({tierCounts.partially_measured})</option>
            <option value="REFERENCE_ONLY">Reference Only ({tierCounts.reference_only})</option>
            <option value="AWAITING_MEASUREMENT">Awaiting Measurement ({tierCounts.awaiting_measurement})</option>
            <option value="DEMO">Demo Sandbox ({tierCounts.demo})</option>
          </select>
        </div>
        <span className="text-xs font-semibold text-slate-600">
          Showing <strong>{questions.length}</strong> validated creator questions
        </span>
      </div>

      {/* Questions Table */}
      <div
        tabIndex={0}
        role="region"
        aria-labelledby="questions-table-caption"
        className="table-wrapper shadow-2xs"
      >
        <table>
          <caption id="questions-table-caption" className="sr-only">
            100 Validated Creator Research Questions with Source Provenance
          </caption>
          <thead>
            <tr className="border-b border-slate-200 text-left text-[11px] font-bold uppercase tracking-wider text-slate-500">
              <th className="py-3 px-4">ID & Canonical Question</th>
              <th className="py-3 px-3">Category & Intent</th>
              <th className="py-3 px-3">Original Wording & Provenance</th>
              <th className="py-3 px-3">Markets</th>
              <th className="py-3 px-3">Priority & Status</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-200 text-xs">
            {questions.map((q) => (
              <tr key={q.id} className="hover:bg-slate-50/80">
                <th scope="row" className="py-3 px-4 text-left font-normal align-top max-w-md">
                  <div className="flex items-center gap-2">
                    <span className="font-mono font-bold text-slate-900">{q.id}</span>
                    <span className="text-[11px] text-slate-500">{q.target_persona}</span>
                    {q.duplicate_merge_count > 0 && (
                      <span className="px-1.5 py-0.5 rounded bg-cyan-100 text-cyan-900 font-semibold text-[10px]">
                        +{q.duplicate_merge_count} Merged Source
                      </span>
                    )}
                  </div>
                  <p className="font-bold text-slate-900 mt-1">{q.canonical_question}</p>
                </th>
                <td className="py-3 px-3 align-top whitespace-nowrap">
                  <span className="font-semibold text-slate-800">{q.category}</span>
                  <span className="block text-[11px] uppercase font-mono text-blue-700 mt-0.5">
                    {q.search_intent}
                  </span>
                </td>
                <td className="py-3 px-3 align-top max-w-sm">
                  <p className="text-slate-600 italic">"{q.original_wording}"</p>
                  <div className="flex items-center gap-2 mt-1 text-[11px] text-slate-500">
                    <a
                      href={q.source_url}
                      target="_blank"
                      rel="noreferrer"
                      className="text-cyan-700 hover:underline inline-flex items-center gap-1 truncate max-w-[200px]"
                    >
                      {q.source_url}
                      <ExternalLink className="w-3 h-3 shrink-0" />
                    </a>
                    <span>· {q.source_type}</span>
                    <span>· {q.collection_date}</span>
                  </div>
                </td>
                <td className="py-3 px-3 align-top whitespace-nowrap">
                  <div className="flex gap-1">
                    {q.target_markets?.map((m: string) => (
                      <span
                        key={m}
                        className="px-1.5 py-0.5 rounded bg-slate-100 text-slate-800 font-mono text-[10px] font-bold"
                      >
                        {m}
                      </span>
                    ))}
                  </div>
                </td>
                <td className="py-3 px-3 align-top whitespace-nowrap">
                  <div className="flex flex-col gap-1">
                    <div className="flex items-center gap-2">
                      <span className="font-mono font-bold text-slate-900">P{q.priority_score}</span>
                      <span className="inline-flex items-center gap-1 px-1.5 py-0.5 rounded text-[10px] font-semibold bg-slate-100 text-slate-700">
                        <CheckCircle2 className="w-3 h-3 text-emerald-600" />
                        {q.validation_status}
                      </span>
                    </div>
                    <span
                      className={`inline-flex items-center justify-center px-2 py-0.5 rounded-full text-[10px] font-semibold border ${
                        q.evidence_tier === 'GENUINE_VERIFIED'
                          ? 'bg-emerald-100 text-emerald-800 border-emerald-300'
                          : q.evidence_tier === 'PARTIALLY_MEASURED'
                          ? 'bg-amber-100 text-amber-800 border-amber-300'
                          : q.evidence_tier === 'REFERENCE_ONLY'
                          ? 'bg-sky-100 text-sky-800 border-sky-300'
                          : q.evidence_tier === 'DEMO'
                          ? 'bg-violet-100 text-violet-800 border-violet-300'
                          : 'bg-slate-100 text-slate-700 border-slate-300'
                      }`}
                    >
                      {q.evidence_tier?.replace(/_/g, ' ')}
                    </span>
                  </div>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};
