import React, { useState, useEffect } from 'react';
import { FileSpreadsheet, RefreshCw, Download, CheckCircle2 } from 'lucide-react';

export const ReportsSection: React.FC = () => {
  const [reports, setReports] = useState<any[]>([]);
  const [workbookBundle, setWorkbookBundle] = useState<any | null>(null);
  const [generating, setGenerating] = useState(false);

  const loadReports = async () => {
    const [repRes, wbRes] = await Promise.all([
      fetch('/api/reports'),
      fetch('/api/exports/workbook'),
    ]);
    const repData = await repRes.json();
    const wbData = await wbRes.json();
    setReports(repData.reports || []);
    setWorkbookBundle(wbData);
  };

  useEffect(() => {
    loadReports();
  }, []);

  const handleRegenerateReport = async () => {
    setGenerating(true);
    try {
      await fetch('/api/reports/generate', { method: 'POST' });
      await loadReports();
    } finally {
      setGenerating(false);
    }
  };

  const handleDownloadMarkdown = (rep: any) => {
    const blob = new Blob([rep.report_markdown], { type: 'text/markdown' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `${rep.report_id}.md`;
    a.click();
    URL.revokeObjectURL(url);
  };

  const latestReport = reports[0];

  return (
    <div className="space-y-6" data-testid="reports-section">
      {/* Header */}
      <div className="bg-white rounded-xl border border-slate-200 p-5 shadow-2xs flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h2 className="text-lg font-bold text-slate-900">
            Weekly Visibility Reports & Official Assessment Workbook Export
          </h2>
          <p className="text-xs text-slate-600 mt-1">
            Summarizes coverage, data quality, multi-date search/AI visibility deltas, competitor mentions, technical fix validations,
            and workbook completeness checks.
          </p>
        </div>
        <div className="flex items-center gap-2 shrink-0">
          <button
            onClick={handleRegenerateReport}
            disabled={generating}
            className="px-3.5 py-2 text-xs font-semibold bg-cyan-600 text-white rounded-lg hover:bg-cyan-700 disabled:opacity-50 inline-flex items-center gap-1.5 cursor-pointer"
          >
            <RefreshCw className={`w-3.5 h-3.5 ${generating ? 'animate-spin' : ''}`} />
            {generating ? 'Generating...' : 'Re-Generate Weekly Report'}
          </button>
          {latestReport && (
            <button
              onClick={() => handleDownloadMarkdown(latestReport)}
              className="px-3.5 py-2 text-xs font-semibold bg-white text-slate-700 border border-slate-300 rounded-lg hover:bg-slate-50 inline-flex items-center gap-1.5 cursor-pointer"
            >
              <Download className="w-3.5 h-3.5" />
              Download Report (.md)
            </button>
          )}
        </div>
      </div>

      {/* Assessment Workbook Completeness Verification Card */}
      {workbookBundle && (
        <div className="bg-white rounded-xl border border-slate-200 p-5 shadow-2xs space-y-3">
          <div className="flex items-center justify-between">
            <h3 className="text-sm font-bold text-slate-900 flex items-center gap-2">
              <FileSpreadsheet className="w-4 h-4 text-emerald-600" />
              Official Assessment Workbook Export Verification (exports/workbook/)
            </h3>
            <span className="text-xs font-mono text-slate-500">
              Generated: {workbookBundle.generated_at}
            </span>
          </div>
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3 text-xs">
            {Object.entries(workbookBundle.completeness_verification || {}).map(([key, val]) => (
              <div
                key={key}
                className="p-3 rounded-lg bg-emerald-50/70 border border-emerald-200 flex items-center justify-between"
              >
                <span className="font-semibold text-emerald-950 capitalize">
                  {key.replace(/_/g, ' ')}
                </span>
                <span className="inline-flex items-center gap-1 px-2 py-0.5 rounded-full text-[11px] font-bold bg-emerald-200 text-emerald-950">
                  <CheckCircle2 className="w-3.5 h-3.5" />
                  {val ? 'VERIFIED' : 'INCOMPLETE'}
                </span>
              </div>
            ))}
          </div>
          <div className="pt-2 border-t border-slate-200 text-xs text-slate-600 flex flex-wrap gap-2">
            <span className="font-semibold text-slate-800">Generated Workbook Tab CSVs:</span>
            {workbookBundle.files_generated?.map((f: string) => (
              <code key={f} className="px-2 py-0.5 bg-slate-100 rounded text-slate-800 font-mono text-[11px]">
                {f}
              </code>
            ))}
          </div>
        </div>
      )}

      {/* Rendered Weekly Markdown Report */}
      {latestReport && (
        <div className="bg-white rounded-xl border border-slate-200 p-6 shadow-2xs space-y-4">
          <div className="flex items-center justify-between border-b border-slate-200 pb-3">
            <div>
              <span className="font-mono text-xs font-bold text-cyan-700">{latestReport.report_id}</span>
              <h3 className="text-base font-bold text-slate-900">{latestReport.report_title}</h3>
            </div>
            <span className="text-xs text-slate-500 font-mono">
              Period: {latestReport.period_start} &rarr; {latestReport.period_end}
            </span>
          </div>
          <pre className="p-4 rounded-xl bg-slate-50 border border-slate-200 font-mono text-xs text-slate-800 whitespace-pre-wrap overflow-x-auto leading-relaxed">
            {latestReport.report_markdown}
          </pre>
        </div>
      )}
    </div>
  );
};
