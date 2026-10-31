import React, { useState, useEffect } from 'react';
import { Award, ExternalLink, CheckCircle2, Filter } from 'lucide-react';

export const CitationsSection: React.FC = () => {
  const [citations, setCitations] = useState<any[]>([]);
  const [sourceTypeFilter, setSourceTypeFilter] = useState('all');
  const [tierFilter, setTierFilter] = useState('all');

  const loadCitations = async () => {
    const params = new URLSearchParams();
    if (sourceTypeFilter !== 'all') params.set('source_type', sourceTypeFilter);
    if (tierFilter !== 'all') params.set('tier', tierFilter);
    const res = await fetch(`/api/citations?${params.toString()}`);
    const data = await res.json();
    setCitations(data.citations || []);
  };

  useEffect(() => {
    loadCitations();
  }, [sourceTypeFilter, tierFilter]);

  return (
    <div className="space-y-6" data-testid="citations-section">
      {/* Header */}
      <div className="bg-white rounded-xl border border-slate-200 p-5 shadow-2xs flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h2 className="text-lg font-bold text-slate-900">
            Third-Party Citation Opportunity Research (30 Specific Target Pages)
          </h2>
          <p className="text-xs text-slate-600 mt-1">
            Prioritizes legitimate software directories (G2, Capterra, Product Hunt, AlternativeTo, Futurepedia),
            comparison articles, editorial guides, and public Reddit/Indie Hackers discussions. Zero automated outreach or third-party edits performed.
          </p>
        </div>
        <div className="flex items-center gap-2 shrink-0">
          <select
            aria-label="Filter by source type"
            value={sourceTypeFilter}
            onChange={(e) => setSourceTypeFilter(e.target.value)}
            className="px-2.5 py-1.5 text-xs bg-slate-50 border border-slate-300 rounded-lg"
          >
            <option value="all">All Source Types</option>
            <option value="directory">Software Directories</option>
            <option value="comparison_article">Comparison Articles</option>
            <option value="editorial_resource">Editorial Resources</option>
            <option value="community_discussion">Community Discussions</option>
            <option value="review_platform">Review Platforms</option>
          </select>

          <select
            aria-label="Filter by priority tier"
            value={tierFilter}
            onChange={(e) => setTierFilter(e.target.value)}
            className="px-2.5 py-1.5 text-xs bg-slate-50 border border-slate-300 rounded-lg"
          >
            <option value="all">All Priority Tiers</option>
            <option value="Tier 1">Tier 1 (Immediate)</option>
            <option value="Tier 2">Tier 2 (Secondary)</option>
            <option value="Tier 3">Tier 3 (Long-Tail)</option>
          </select>
        </div>
      </div>

      {/* Responsive Table */}
      <div
        tabIndex={0}
        role="region"
        aria-labelledby="citations-table-caption"
        className="table-wrapper shadow-2xs"
      >
        <table>
          <caption id="citations-table-caption" className="sr-only">
            30 researched third-party citation opportunities for IncuBrix
          </caption>
          <thead>
            <tr className="border-b border-slate-200 text-left text-[11px] font-bold uppercase tracking-wider text-slate-500">
              <th className="py-3 px-4">ID / Page Title & Exact URL</th>
              <th className="py-3 px-3">Publisher & Type</th>
              <th className="py-3 px-3">Relevant Topic & Evidence</th>
              <th className="py-3 px-3">Competitors Observed</th>
              <th className="py-3 px-4">Suitability & Policy-Compliant Angle</th>
              <th className="py-3 px-3">Status</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-200 text-xs">
            {citations.map((cit) => (
              <tr key={cit.opportunity_id} className="hover:bg-slate-50/80">
                <th scope="row" className="py-3 px-4 text-left font-normal align-top max-w-xs">
                  <div className="flex items-center gap-2">
                    <span className="font-mono font-bold text-slate-900">{cit.opportunity_id}</span>
                    <span className="px-1.5 py-0.5 rounded text-[10px] font-bold bg-indigo-50 text-indigo-800 border border-indigo-200">
                      {cit.priority_tier}
                    </span>
                  </div>
                  <p className="font-bold text-slate-900 mt-1">{cit.page_title}</p>
                  <a
                    href={cit.page_url}
                    target="_blank"
                    rel="noreferrer"
                    className="font-mono text-[11px] text-cyan-700 hover:underline inline-flex items-center gap-1 mt-0.5 break-all"
                  >
                    {cit.page_url}
                    <ExternalLink className="w-3 h-3 shrink-0" />
                  </a>
                </th>
                <td className="py-3 px-3 align-top whitespace-nowrap">
                  <span className="font-bold text-slate-900">{cit.publisher_domain}</span>
                  <span className="block text-[11px] text-slate-500 capitalize mt-0.5">
                    {cit.source_type.replace(/_/g, ' ')}
                  </span>
                  <span className="block text-[10px] font-mono text-slate-400 mt-0.5">
                    Researched: {cit.research_date}
                  </span>
                </td>
                <td className="py-3 px-3 align-top max-w-xs">
                  <span className="font-semibold text-slate-800">
                    [{cit.relevant_question_id}] {cit.relevant_topic}
                  </span>
                  <p className="text-slate-600 mt-1 leading-relaxed">{cit.evidence_of_relevance}</p>
                </td>
                <td className="py-3 px-3 align-top max-w-[170px]">
                  <div className="flex flex-wrap gap-1">
                    {cit.competitor_mentions?.map((c: string) => (
                      <span
                        key={c}
                        className="px-1.5 py-0.5 rounded bg-slate-100 text-slate-700 text-[11px] font-medium"
                      >
                        {c}
                      </span>
                    ))}
                  </div>
                  <span className="block text-[10px] text-slate-500 mt-1">
                    IncuBrix Mentioned: <strong>{cit.incubrix_currently_mentioned ? 'Yes' : 'No'}</strong>
                  </span>
                </td>
                <td className="py-3 px-4 align-top max-w-sm space-y-1">
                  <p className="text-slate-700">
                    <strong>Why Suitable:</strong> {cit.suitability_rationale}
                  </p>
                  <p className="text-emerald-900 bg-emerald-50/70 p-2 rounded border border-emerald-200">
                    <strong>Compliant Angle:</strong> {cit.outreach_angle}
                  </p>
                </td>
                <td className="py-3 px-3 align-top whitespace-nowrap">
                  <span className="inline-flex items-center gap-1 px-2 py-0.5 rounded-full text-[11px] font-semibold bg-emerald-100 text-emerald-800 border border-emerald-300">
                    <CheckCircle2 className="w-3 h-3" />
                    {cit.verification_status}
                  </span>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};
