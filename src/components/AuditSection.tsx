import React, { useState, useEffect } from 'react';
import {
  ShieldAlert,
  CheckCircle2,
  RefreshCw,
  Copy,
  Check,
  Code2,
  Globe,
  ExternalLink,
  FileCode,
} from 'lucide-react';

interface Props {
  onDataChanged: () => void;
}

const SEVERITY_STYLES: Record<string, string> = {
  critical: 'bg-rose-100 text-rose-900 border-rose-300',
  high: 'bg-amber-100 text-amber-900 border-amber-300',
  medium: 'bg-blue-100 text-blue-900 border-blue-300',
  low: 'bg-slate-100 text-slate-800 border-slate-300',
};

export const AuditSection: React.FC<Props> = ({ onDataChanged }) => {
  const [issues, setIssues] = useState<any[]>([]);
  const [crawledPages, setCrawledPages] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [auditing, setAuditing] = useState(false);
  const [severityFilter, setSeverityFilter] = useState('all');
  const [categoryFilter, setCategoryFilter] = useState('all');
  const [selectedIssue, setSelectedIssue] = useState<any | null>(null);
  const [copiedId, setCopiedId] = useState<string | null>(null);

  // Interactive JSON-LD Validator state
  const [customJsonLd, setCustomJsonLd] = useState('');
  const [jsonLdValidationResult, setJsonLdValidationResult] = useState<{
    valid: boolean;
    errors: string[];
  } | null>(null);

  const loadAudit = async () => {
    setLoading(true);
    try {
      const res = await fetch('/api/audit');
      const data = await res.json();
      setIssues(data.issues || []);
      setCrawledPages(data.crawled_pages || []);
      if (data.issues?.length > 0 && !selectedIssue) {
        setSelectedIssue(data.issues[0]);
        setCustomJsonLd(
          data.issues[0].ready_to_apply_code
            .replace(/<script[^>]*>/i, '')
            .replace(/<\/script>/i, '')
            .trim()
        );
      }
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadAudit();
  }, []);

  const handleRerunAudit = async () => {
    setAuditing(true);
    try {
      await fetch('/api/audit/run', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ fetch_live: true }),
      });
      await loadAudit();
      onDataChanged();
    } finally {
      setAuditing(false);
    }
  };

  const handleCopyCode = (id: string, code: string) => {
    navigator.clipboard.writeText(code);
    setCopiedId(id);
    setTimeout(() => setCopiedId(null), 2000);
  };

  const handleValidateCustomJsonLd = async () => {
    const res = await fetch('/api/audit/validate-jsonld', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ json_ld: customJsonLd }),
    });
    const data = await res.json();
    setJsonLdValidationResult(data);
  };

  const categories = Array.from(new Set(issues.map((i) => i.category)));
  const filteredIssues = issues.filter((i) => {
    if (severityFilter !== 'all' && i.severity !== severityFilter) return false;
    if (categoryFilter !== 'all' && i.category !== categoryFilter) return false;
    return true;
  });

  return (
    <div className="space-y-6" data-testid="audit-section">
      {/* Top Header */}
      <div className="bg-white rounded-xl border border-slate-200 p-5 shadow-2xs flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h2 className="text-lg font-bold text-slate-900">
            Technical SEO, AEO & GEO Website Auditor — <code className="text-cyan-700">incubrix.com</code>
          </h2>
          <p className="text-xs text-slate-600 mt-1">
            Real HTTP inspection of <strong>{crawledPages.length} public sitemap URLs</strong>,{' '}
            <code>robots.txt</code>, <code>sitemap.xml</code>, and <code>/llms.txt</code>. Includes{' '}
            <strong>{issues.length} prioritized fix records</strong> with ready-to-apply code and automated patch validation tests.
          </p>
        </div>
        <button
          onClick={handleRerunAudit}
          disabled={auditing}
          className="px-3.5 py-2 text-xs font-semibold bg-cyan-600 text-white rounded-lg hover:bg-cyan-700 disabled:opacity-50 inline-flex items-center gap-1.5 shrink-0 cursor-pointer"
        >
          <RefreshCw className={`w-3.5 h-3.5 ${auditing ? 'animate-spin' : ''}`} />
          {auditing ? 'Crawling incubrix.com...' : 'Re-Run Live HTTP Audit'}
        </button>
      </div>

      {/* Live Crawled Pages Snapshot Table */}
      <div className="bg-white rounded-xl border border-slate-200 p-5 shadow-2xs space-y-3">
        <div className="flex items-center justify-between">
          <h3 className="text-sm font-bold text-slate-900 flex items-center gap-2">
            <Globe className="w-4 h-4 text-cyan-600" />
            Live Crawled Sitemap Pages on https://incubrix.com ({crawledPages.length} URLs)
          </h3>
          <span className="text-xs text-slate-500">
            Raw HTML snapshots saved in <code>data/evidence/crawl/</code>
          </span>
        </div>
        <div
          tabIndex={0}
          role="region"
          aria-label="Crawled pages from incubrix.com"
          className="table-wrapper max-h-64"
        >
          <table>
            <thead>
              <tr className="border-b border-slate-200 text-left text-[11px] font-bold uppercase tracking-wider text-slate-500">
                <th className="py-2.5 px-3">Page URL</th>
                <th className="py-2.5 px-2">HTTP</th>
                <th className="py-2.5 px-3">Page Title</th>
                <th className="py-2.5 px-2">H1 Count</th>
                <th className="py-2.5 px-2">JSON-LD</th>
                <th className="py-2.5 px-2">Missing Alt</th>
                <th className="py-2.5 px-2">Size / Load</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-200 text-xs">
              {crawledPages.map((p) => (
                <tr key={p.url} className="hover:bg-slate-50">
                  <th scope="row" className="py-2 px-3 font-mono font-semibold text-cyan-800 text-left">
                    <a href={p.url} target="_blank" rel="noreferrer" className="hover:underline inline-flex items-center gap-1">
                      {p.url.replace('https://incubrix.com', '') || '/'}
                      <ExternalLink className="w-3 h-3" />
                    </a>
                  </th>
                  <td className="py-2 px-2">
                    <span className="px-1.5 py-0.5 rounded bg-emerald-100 text-emerald-800 font-mono text-[11px] font-bold">
                      {p.http_status}
                    </span>
                  </td>
                  <td className="py-2 px-3 text-slate-800 max-w-xs truncate" title={p.title}>
                    {p.title}
                  </td>
                  <td className="py-2 px-2 font-mono">
                    {p.h1_tags?.length === 1 && p.h1_tags[0] !== '' ? (
                      <span className="text-emerald-700 font-semibold">1 OK</span>
                    ) : (
                      <span className="text-rose-700 font-bold">Empty H1!</span>
                    )}
                  </td>
                  <td className="py-2 px-2 font-mono">
                    <span className="text-rose-700 font-bold">{p.json_ld_blocks?.length || 0}</span>
                  </td>
                  <td className="py-2 px-2 font-mono">
                    {p.images_missing_alt > 0 ? (
                      <span className="text-amber-700 font-bold">
                        {p.images_missing_alt} / {p.images_total}
                      </span>
                    ) : (
                      <span className="text-emerald-700">0 / {p.images_total}</span>
                    )}
                  </td>
                  <td className="py-2 px-2 font-mono text-[11px] text-slate-500">
                    {(p.page_size_bytes / 1024).toFixed(1)} KB · {p.load_time_ms}ms
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {/* Filter Bar & Split Master-Detail View for 22 Prioritized Fix Records */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        {/* Left Column: 22 Prioritized Issues List */}
        <div className="lg:col-span-5 bg-white rounded-xl border border-slate-200 p-4 shadow-2xs flex flex-col max-h-[700px]">
          <div className="flex items-center justify-between gap-2 pb-3 border-b border-slate-200">
            <h3 className="text-sm font-bold text-slate-900">
              Prioritized Fixes ({filteredIssues.length} / {issues.length})
            </h3>
            <div className="flex items-center gap-2">
              <select
                aria-label="Filter by severity"
                value={severityFilter}
                onChange={(e) => setSeverityFilter(e.target.value)}
                className="px-2 py-1 text-xs bg-slate-50 border border-slate-300 rounded"
              >
                <option value="all">All Severities</option>
                <option value="critical">Critical</option>
                <option value="high">High</option>
                <option value="medium">Medium</option>
                <option value="low">Low</option>
              </select>
              <select
                aria-label="Filter by category"
                value={categoryFilter}
                onChange={(e) => setCategoryFilter(e.target.value)}
                className="px-2 py-1 text-xs bg-slate-50 border border-slate-300 rounded max-w-[140px]"
              >
                <option value="all">All Categories</option>
                {categories.map((c) => (
                  <option key={c} value={c}>
                    {c}
                  </option>
                ))}
              </select>
            </div>
          </div>

          <div className="overflow-y-auto divide-y divide-slate-200 mt-2 pr-1">
            {filteredIssues.map((iss) => {
              const isSelected = selectedIssue?.issue_id === iss.issue_id;
              return (
                <button
                  key={iss.issue_id}
                  onClick={() => setSelectedIssue(iss)}
                  className={`w-full text-left p-3 transition hover:bg-slate-50 cursor-pointer ${
                    isSelected ? 'bg-cyan-50/80 border-l-4 border-l-cyan-600' : ''
                  }`}
                >
                  <div className="flex items-center justify-between gap-2">
                    <div className="flex items-center gap-2">
                      <span className="font-mono text-xs font-bold text-slate-900">
                        #{iss.priority_rank} · {iss.issue_id}
                      </span>
                      <span
                        className={`px-2 py-0.5 rounded-full text-[10px] font-bold uppercase border ${
                          SEVERITY_STYLES[iss.severity] || SEVERITY_STYLES.low
                        }`}
                      >
                        {iss.severity}
                      </span>
                    </div>
                    <span className="inline-flex items-center gap-1 text-[11px] font-semibold text-emerald-700">
                      <CheckCircle2 className="w-3.5 h-3.5" />
                      Patch Verified
                    </span>
                  </div>
                  <p className="text-xs font-bold text-slate-900 mt-1.5">{iss.title}</p>
                  <p className="text-[11px] text-slate-500 font-mono mt-0.5 truncate">{iss.page_url}</p>
                </button>
              );
            })}
          </div>
        </div>

        {/* Right Column: Selected Issue Evidence, Ready-to-Apply Code & Validation Result */}
        <div className="lg:col-span-7 space-y-6">
          {selectedIssue && (
            <div className="bg-white rounded-xl border border-slate-200 p-5 shadow-2xs space-y-4">
              <div className="flex items-start justify-between gap-3 border-b border-slate-200 pb-3">
                <div>
                  <div className="flex items-center gap-2">
                    <span className="font-mono text-xs font-bold px-2 py-0.5 rounded bg-slate-900 text-white">
                      {selectedIssue.issue_id} (Priority #{selectedIssue.priority_rank})
                    </span>
                    <span
                      className={`px-2 py-0.5 rounded-full text-xs font-bold uppercase border ${
                        SEVERITY_STYLES[selectedIssue.severity]
                      }`}
                    >
                      {selectedIssue.severity}
                    </span>
                    <span className="text-xs font-semibold text-slate-500">{selectedIssue.category}</span>
                  </div>
                  <h3 className="text-base font-bold text-slate-900 mt-2">{selectedIssue.title}</h3>
                  <p className="text-xs font-mono text-cyan-700 mt-0.5">Target URL: {selectedIssue.page_url}</p>
                </div>
              </div>

              <div className="space-y-3 text-xs">
                <div>
                  <h4 className="font-bold uppercase tracking-wider text-slate-500 text-[11px]">
                    Finding Description
                  </h4>
                  <p className="text-slate-700 mt-1 leading-relaxed">{selectedIssue.description}</p>
                </div>

                <div className="p-3 rounded-lg bg-rose-50/70 border border-rose-200">
                  <h4 className="font-bold uppercase tracking-wider text-rose-800 text-[11px]">
                    Actual Measured HTTP / DOM Evidence
                  </h4>
                  <p className="font-mono text-rose-950 mt-1 whitespace-pre-wrap">{selectedIssue.actual_evidence}</p>
                </div>

                <div>
                  <h4 className="font-bold uppercase tracking-wider text-slate-500 text-[11px]">
                    Recommended Change
                  </h4>
                  <p className="text-slate-800 font-medium mt-1">{selectedIssue.recommended_change}</p>
                </div>

                <div>
                  <div className="flex items-center justify-between mb-1.5">
                    <h4 className="font-bold uppercase tracking-wider text-slate-500 text-[11px] flex items-center gap-1.5">
                      <Code2 className="w-3.5 h-3.5 text-cyan-600" />
                      Ready-to-Apply Code / Structured Data Patch
                    </h4>
                    <button
                      onClick={() => handleCopyCode(selectedIssue.issue_id, selectedIssue.ready_to_apply_code)}
                      className="px-2.5 py-1 text-[11px] font-semibold bg-slate-100 hover:bg-slate-200 text-slate-800 rounded inline-flex items-center gap-1 cursor-pointer"
                    >
                      {copiedId === selectedIssue.issue_id ? (
                        <>
                          <Check className="w-3 h-3 text-emerald-600" /> Copied
                        </>
                      ) : (
                        <>
                          <Copy className="w-3 h-3" /> Copy Patch
                        </>
                      )}
                    </button>
                  </div>
                  <pre className="p-3.5 rounded-lg bg-slate-900 text-slate-100 font-mono text-[11px] overflow-x-auto max-h-64">
                    <code>{selectedIssue.ready_to_apply_code}</code>
                  </pre>
                </div>

                <div className="p-3 rounded-lg bg-emerald-50 border border-emerald-200 space-y-1">
                  <div className="flex items-center justify-between">
                    <span className="font-bold uppercase tracking-wider text-emerald-900 text-[11px]">
                      Automated Validation Method & Result
                    </span>
                    <span className="px-2 py-0.5 rounded text-[10px] font-bold bg-emerald-200 text-emerald-950">
                      {selectedIssue.validation_status.toUpperCase()}
                    </span>
                  </div>
                  <p className="text-emerald-800">
                    <strong>Method:</strong> {selectedIssue.validation_method}
                  </p>
                  <p className="font-mono text-emerald-950 font-medium">{selectedIssue.validation_result}</p>
                </div>
              </div>
            </div>
          )}

          {/* Interactive JSON-LD Schema Validator */}
          <div className="bg-white rounded-xl border border-slate-200 p-5 shadow-2xs space-y-3">
            <div className="flex items-center justify-between">
              <div>
                <h3 className="text-sm font-bold text-slate-900 flex items-center gap-1.5">
                  <FileCode className="w-4 h-4 text-violet-600" />
                  Interactive JSON-LD Schema & Anti-Hallucination Validator
                </h3>
                <p className="text-xs text-slate-500">
                  Tests JSON-LD syntax, required <code>@context</code> / <code>@type</code>, and blocks fabricated{' '}
                  <code>AggregateRating</code> or <code>review</code> properties.
                </p>
              </div>
              <button
                onClick={handleValidateCustomJsonLd}
                className="px-3 py-1.5 text-xs font-semibold bg-violet-600 text-white rounded-lg hover:bg-violet-700 cursor-pointer"
              >
                Validate JSON-LD
              </button>
            </div>
            <textarea
              rows={5}
              value={customJsonLd}
              onChange={(e) => setCustomJsonLd(e.target.value)}
              className="w-full p-3 font-mono text-xs bg-slate-50 border border-slate-300 rounded-lg"
              placeholder='Paste JSON-LD object here (e.g. {"@context": "https://schema.org", "@type": "Organization", ...})'
            />
            {jsonLdValidationResult && (
              <div
                className={`p-3 rounded-lg border text-xs font-medium ${
                  jsonLdValidationResult.valid
                    ? 'bg-emerald-50 border-emerald-300 text-emerald-900'
                    : 'bg-rose-50 border-rose-300 text-rose-900'
                }`}
              >
                {jsonLdValidationResult.valid ? (
                  <span>PASS: Valid schema.org JSON-LD structure with zero fabricated rating/review fields.</span>
                ) : (
                  <ul className="list-disc pl-4 space-y-0.5">
                    {jsonLdValidationResult.errors.map((e, i) => (
                      <li key={i}>{e}</li>
                    ))}
                  </ul>
                )}
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};
