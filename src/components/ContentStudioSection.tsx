import React, { useState, useEffect } from 'react';
import {
  FileText,
  CheckCircle2,
  AlertTriangle,
  Download,
  Sparkles,
  Save,
  ExternalLink,
  Link2,
  Code2,
} from 'lucide-react';

interface Props {
  onDataChanged: () => void;
}

const CONTENT_TYPE_LABELS: Record<string, string> = {
  how_to_guide: 'How-To Guide',
  product_comparison: 'Product Comparison',
  faq_page: 'FAQ Page',
  glossary_entry: 'Glossary Entry',
  problem_solving_guide: 'Problem-Solving Guide',
};

export const ContentStudioSection: React.FC<Props> = ({ onDataChanged }) => {
  const [pages, setPages] = useState<any[]>([]);
  const [selectedPage, setSelectedPage] = useState<any | null>(null);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [feedback, setFeedback] = useState<string | null>(null);

  // Brief generator state
  const [briefQid, setBriefQid] = useState('Q-019');
  const [briefType, setBriefType] = useState('how_to_guide');
  const [generatedBrief, setGeneratedBrief] = useState<any | null>(null);

  const loadPages = async () => {
    setLoading(true);
    try {
      const res = await fetch('/api/content');
      const data = await res.json();
      const list = data.pages || [];
      setPages(list);
      if (list.length > 0 && !selectedPage) {
        setSelectedPage(list[0]);
      }
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadPages();
  }, []);

  const handleSavePage = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!selectedPage) return;
    setSaving(true);
    setFeedback(null);
    try {
      const res = await fetch(`/api/content/${selectedPage.page_id}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          title: selectedPage.title,
          meta_description: selectedPage.meta_description,
          direct_answer_summary: selectedPage.direct_answer_summary,
          body_markdown: selectedPage.body_markdown,
          json_ld_schema: selectedPage.json_ld_schema,
          status: selectedPage.status,
        }),
      });
      if (!res.ok) {
        const err = await res.json();
        throw new Error(err.error || 'Failed to save page');
      }
      setFeedback(`Saved ${selectedPage.page_id} and exported updated Markdown/HTML files to exports/content_pages/.`);
      await loadPages();
      onDataChanged();
    } catch (err: any) {
      setFeedback(`Validation error: ${err.message}`);
    } finally {
      setSaving(false);
    }
  };

  const handleExportDownload = async (pageId: string, format: 'md' | 'html') => {
    const res = await fetch(`/api/content/${pageId}/export`);
    const data = await res.json();
    const content = format === 'md' ? data.markdown_content : data.html_content;
    const blob = new Blob([content], { type: format === 'md' ? 'text/markdown' : 'text/html' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `${selectedPage?.slug || pageId}.${format}`;
    a.click();
    URL.revokeObjectURL(url);
  };

  const handleGenerateBrief = async () => {
    const res = await fetch('/api/content/generate-brief', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ question_id: briefQid, content_type: briefType }),
    });
    const data = await res.json();
    setGeneratedBrief(data);
  };

  return (
    <div className="space-y-6" data-testid="content-section">
      {/* Header */}
      <div className="bg-white rounded-xl border border-slate-200 p-5 shadow-2xs flex flex-col lg:flex-row lg:items-center justify-between gap-4">
        <div>
          <h2 className="text-lg font-bold text-slate-900">
            Content Studio — 10 Publish-Ready AEO / GEO Pages & Brief Generator
          </h2>
          <p className="text-xs text-slate-600 mt-1">
            Every page includes a 2-sentence direct answer, verified product facts, source citations, internal links,
            JSON-LD schema, and human-review flags for unshipped features (never auto-publishes to live site).
          </p>
        </div>
        <div className="flex items-center gap-2">
          {selectedPage && (
            <>
              <button
                onClick={() => handleExportDownload(selectedPage.page_id, 'md')}
                className="px-3 py-1.5 text-xs font-semibold bg-white text-slate-700 border border-slate-300 rounded-lg hover:bg-slate-50 inline-flex items-center gap-1.5 cursor-pointer"
              >
                <Download className="w-3.5 h-3.5" /> Export Markdown (.md)
              </button>
              <button
                onClick={() => handleExportDownload(selectedPage.page_id, 'html')}
                className="px-3 py-1.5 text-xs font-semibold bg-cyan-600 text-white rounded-lg hover:bg-cyan-700 inline-flex items-center gap-1.5 cursor-pointer"
              >
                <Download className="w-3.5 h-3.5" /> Export Standalone HTML (.html)
              </button>
            </>
          )}
        </div>
      </div>

      {feedback && (
        <div className="p-3 rounded-lg bg-cyan-50 border border-cyan-200 text-xs font-medium text-cyan-950 flex items-center justify-between">
          <span>{feedback}</span>
          <button onClick={() => setFeedback(null)} className="font-bold text-cyan-800 cursor-pointer">
            Dismiss
          </button>
        </div>
      )}

      {/* Split Layout: 10 Pages List + Full Editor & Verification Panel */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        {/* Left List of 10 Pages */}
        <div className="lg:col-span-4 bg-white rounded-xl border border-slate-200 p-4 shadow-2xs space-y-2 max-h-[820px] overflow-y-auto">
          <h3 className="text-xs font-bold uppercase tracking-wider text-slate-500 pb-2 border-b border-slate-200">
            10 Validated Content Pages ({pages.length})
          </h3>
          {pages.map((p) => {
            const isSelected = selectedPage?.page_id === p.page_id;
            return (
              <button
                key={p.page_id}
                onClick={() => setSelectedPage(p)}
                className={`w-full text-left p-3 rounded-lg border transition cursor-pointer ${
                  isSelected
                    ? 'bg-cyan-50/90 border-cyan-500 shadow-2xs'
                    : 'bg-white border-slate-200 hover:bg-slate-50'
                }`}
              >
                <div className="flex items-center justify-between gap-2">
                  <span className="font-mono text-xs font-bold text-slate-900">{p.page_id}</span>
                  <span
                    className={`px-2 py-0.5 rounded-full text-[10px] font-bold uppercase ${
                      p.status === 'ready_to_publish'
                        ? 'bg-emerald-100 text-emerald-800'
                        : p.status === 'reviewed'
                        ? 'bg-blue-100 text-blue-800'
                        : 'bg-slate-100 text-slate-700'
                    }`}
                  >
                    {p.status.replace(/_/g, ' ')}
                  </span>
                </div>
                <p className="text-xs font-bold text-slate-900 mt-1 line-clamp-2">{p.title}</p>
                <div className="flex items-center justify-between text-[11px] text-slate-500 mt-1.5">
                  <span>{CONTENT_TYPE_LABELS[p.content_type] || p.content_type}</span>
                  <span className="font-mono">{p.word_count} words</span>
                </div>
              </button>
            );
          })}
        </div>

        {/* Right Editor & Verification Inspector */}
        <div className="lg:col-span-8 space-y-6">
          {selectedPage && (
            <form
              onSubmit={handleSavePage}
              className="bg-white rounded-xl border border-slate-200 p-5 shadow-2xs space-y-4"
            >
              <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 border-b border-slate-200 pb-3">
                <div>
                  <span className="text-xs font-mono font-bold text-cyan-700">
                    {selectedPage.page_id} · /{selectedPage.slug}
                  </span>
                  <p className="text-xs text-slate-500 mt-0.5">
                    Audience: <strong>{selectedPage.target_audience}</strong> · Intent:{' '}
                    <strong className="uppercase">{selectedPage.search_intent}</strong>
                  </p>
                </div>
                <div className="flex items-center gap-2">
                  <select
                    aria-label="Page Status"
                    value={selectedPage.status}
                    onChange={(e) => setSelectedPage({ ...selectedPage, status: e.target.value })}
                    className="px-2.5 py-1.5 text-xs font-semibold bg-slate-50 border border-slate-300 rounded-lg"
                  >
                    <option value="draft">Draft</option>
                    <option value="reviewed">Reviewed</option>
                    <option value="ready_to_publish">Ready to Publish</option>
                  </select>
                  <button
                    type="submit"
                    disabled={saving}
                    className="px-3.5 py-1.5 text-xs font-semibold bg-emerald-600 text-white rounded-lg hover:bg-emerald-700 inline-flex items-center gap-1.5 cursor-pointer"
                  >
                    <Save className="w-3.5 h-3.5" />
                    {saving ? 'Saving...' : 'Save & Validate'}
                  </button>
                </div>
              </div>

              <div className="grid grid-cols-1 gap-3 text-xs">
                <div>
                  <label className="block font-bold text-slate-700 mb-1">Page Title</label>
                  <input
                    type="text"
                    value={selectedPage.title}
                    onChange={(e) => setSelectedPage({ ...selectedPage, title: e.target.value })}
                    className="w-full px-3 py-1.5 bg-slate-50 border border-slate-300 rounded-lg font-semibold text-slate-900"
                  />
                </div>

                <div>
                  <label className="block font-bold text-slate-700 mb-1">
                    Meta Description ({selectedPage.meta_description?.length || 0} / 170 chars)
                  </label>
                  <input
                    type="text"
                    value={selectedPage.meta_description}
                    onChange={(e) => setSelectedPage({ ...selectedPage, meta_description: e.target.value })}
                    className="w-full px-3 py-1.5 bg-slate-50 border border-slate-300 rounded-lg text-slate-800"
                  />
                </div>

                <div className="p-3 rounded-lg bg-cyan-50/70 border border-cyan-200">
                  <label className="block font-bold text-cyan-950 mb-1">
                    Direct 2-Sentence AEO Answer (First Two Sentences)
                  </label>
                  <textarea
                    rows={3}
                    value={selectedPage.direct_answer_summary}
                    onChange={(e) => setSelectedPage({ ...selectedPage, direct_answer_summary: e.target.value })}
                    className="w-full p-2 bg-white border border-cyan-300 rounded text-slate-900 leading-relaxed"
                  />
                </div>

                <div>
                  <label className="block font-bold text-slate-700 mb-1">
                    Body Content (Markdown Editor)
                  </label>
                  <textarea
                    rows={12}
                    value={selectedPage.body_markdown}
                    onChange={(e) => setSelectedPage({ ...selectedPage, body_markdown: e.target.value })}
                    className="w-full p-3 font-mono text-xs bg-slate-50 border border-slate-300 rounded-lg leading-relaxed"
                  />
                </div>

                {/* Citations & Internal Links */}
                <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                  <div className="p-3 rounded-lg bg-slate-50 border border-slate-200 space-y-1.5">
                    <h4 className="font-bold text-slate-700 flex items-center gap-1.5">
                      <ExternalLink className="w-3.5 h-3.5 text-cyan-600" />
                      Verifiable Citations & Source URLs
                    </h4>
                    <ul className="space-y-1">
                      {selectedPage.citations?.map((c: any, idx: number) => (
                        <li key={idx} className="truncate">
                          <a
                            href={c.url}
                            target="_blank"
                            rel="noreferrer"
                            className="text-cyan-700 hover:underline font-medium"
                          >
                            {c.label}
                          </a>
                          <span className="block text-[10px] font-mono text-slate-400">{c.url}</span>
                        </li>
                      ))}
                    </ul>
                  </div>

                  <div className="p-3 rounded-lg bg-slate-50 border border-slate-200 space-y-1.5">
                    <h4 className="font-bold text-slate-700 flex items-center gap-1.5">
                      <Link2 className="w-3.5 h-3.5 text-blue-600" />
                      Internal-Link Recommendations
                    </h4>
                    <ul className="space-y-1">
                      {selectedPage.internal_links?.map((l: any, idx: number) => (
                        <li key={idx}>
                          <span className="font-semibold text-slate-800">{l.anchor}</span>
                          <span className="block text-[10px] font-mono text-blue-700">{l.url}</span>
                        </li>
                      ))}
                    </ul>
                  </div>
                </div>

                {/* Factual Verification Checklist & Unverified Claim Flags */}
                <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                  <div className="p-3 rounded-lg bg-emerald-50/70 border border-emerald-200 space-y-1.5">
                    <h4 className="font-bold text-emerald-950 flex items-center gap-1.5">
                      <CheckCircle2 className="w-3.5 h-3.5 text-emerald-600" />
                      Factual Verification Checklist
                    </h4>
                    <ul className="space-y-1">
                      {selectedPage.verification_checklist?.map((chk: any, idx: number) => (
                        <li key={idx} className="flex items-start gap-1.5 text-emerald-900">
                          <span className="font-bold text-emerald-600">&#10003;</span>
                          <span>{chk.item}</span>
                        </li>
                      ))}
                    </ul>
                  </div>

                  <div className="p-3 rounded-lg bg-amber-50/70 border border-amber-200 space-y-1.5">
                    <h4 className="font-bold text-amber-950 flex items-center gap-1.5">
                      <AlertTriangle className="w-3.5 h-3.5 text-amber-600" />
                      Human-Review Flags (Unshipped / Coming Soon Claims)
                    </h4>
                    {selectedPage.unverified_claims_flagged?.length > 0 ? (
                      <ul className="space-y-1 text-amber-900 list-disc pl-4">
                        {selectedPage.unverified_claims_flagged.map((fl: string, idx: number) => (
                          <li key={idx}>{fl}</li>
                        ))}
                      </ul>
                    ) : (
                      <p className="text-amber-800">
                        All product claims on this page match currently live features on <code>incubrix.com</code>.
                      </p>
                    )}
                  </div>
                </div>

                <div>
                  <label className="block font-bold text-slate-700 mb-1 flex items-center gap-1.5">
                    <Code2 className="w-3.5 h-3.5 text-violet-600" />
                    Embedded Page JSON-LD Schema
                  </label>
                  <textarea
                    rows={6}
                    value={selectedPage.json_ld_schema}
                    onChange={(e) => setSelectedPage({ ...selectedPage, json_ld_schema: e.target.value })}
                    className="w-full p-2.5 font-mono text-[11px] bg-slate-900 text-slate-100 rounded-lg"
                  />
                </div>
              </div>
            </form>
          )}

          {/* New Content Brief Generator */}
          <div className="bg-white rounded-xl border border-slate-200 p-5 shadow-2xs space-y-3">
            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
              <div>
                <h3 className="text-sm font-bold text-slate-900 flex items-center gap-1.5">
                  <Sparkles className="w-4 h-4 text-indigo-600" />
                  Automated Content Brief Generator (For Any of the 100 Creator Questions)
                </h3>
                <p className="text-xs text-slate-500">
                  Generates a structured AEO/GEO brief with 2-sentence direct answer starter, headings, JSON-LD, and claim guardrails.
                </p>
              </div>
              <div className="flex items-center gap-2">
                <input
                  type="text"
                  value={briefQid}
                  onChange={(e) => setBriefQid(e.target.value)}
                  className="w-24 px-2.5 py-1.5 text-xs font-mono bg-slate-50 border border-slate-300 rounded-lg"
                  placeholder="Q-019"
                />
                <select
                  value={briefType}
                  onChange={(e) => setBriefType(e.target.value)}
                  className="px-2.5 py-1.5 text-xs bg-slate-50 border border-slate-300 rounded-lg"
                >
                  <option value="how_to_guide">How-To Guide</option>
                  <option value="product_comparison">Product Comparison</option>
                  <option value="faq_page">FAQ Page</option>
                  <option value="glossary_entry">Glossary Entry</option>
                  <option value="problem_solving_guide">Problem-Solving Guide</option>
                </select>
                <button
                  type="button"
                  onClick={handleGenerateBrief}
                  className="px-3 py-1.5 text-xs font-semibold bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 cursor-pointer"
                >
                  Generate Brief
                </button>
              </div>
            </div>

            {generatedBrief && (
              <div className="p-4 rounded-lg bg-indigo-50/60 border border-indigo-200 text-xs space-y-2">
                <div className="flex items-center justify-between">
                  <span className="font-mono font-bold text-indigo-950">
                    {generatedBrief.question_id}: {generatedBrief.canonical_question}
                  </span>
                  <span className="px-2 py-0.5 rounded bg-indigo-200 text-indigo-900 font-semibold">
                    /{generatedBrief.recommended_slug}
                  </span>
                </div>
                <p className="text-slate-800">
                  <strong>2-Sentence Direct Answer Draft:</strong> {generatedBrief.direct_answer_draft}
                </p>
                <p className="text-slate-700">
                  <strong>Recommended Headings:</strong> {generatedBrief.recommended_headings?.join(' -> ')}
                </p>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};
