import React, { useState, useEffect } from 'react';
import { Settings, Key, Terminal, Clock, CheckCircle2, AlertCircle } from 'lucide-react';

export const SettingsSection: React.FC = () => {
  const [settings, setSettings] = useState<any | null>(null);

  useEffect(() => {
    fetch('/api/settings')
      .then((r) => r.json())
      .then((d) => setSettings(d));
  }, []);

  if (!settings) {
    return <div className="p-6 bg-white rounded-xl border border-slate-200 text-xs">Loading settings...</div>;
  }

  return (
    <div className="space-y-6" data-testid="settings-section">
      {/* Header */}
      <div className="bg-white rounded-xl border border-slate-200 p-5 shadow-2xs">
        <h2 className="text-lg font-bold text-slate-900">
          Settings, Pluggable Provider Adapters & Windows Task Scheduler Automation
        </h2>
        <p className="text-xs text-slate-600 mt-1">
          Core features operate without paid API keys. When keys are configured in <code>.env</code>, live automated SERP and LLM
          adapters activate automatically.
        </p>
      </div>

      {/* Pluggable Provider Adapters Status */}
      <div className="bg-white rounded-xl border border-slate-200 p-5 shadow-2xs space-y-3">
        <h3 className="text-sm font-bold text-slate-900 flex items-center gap-2">
          <Key className="w-4 h-4 text-cyan-600" />
          Search & AI Assistant Provider Adapters (5 Integrations)
        </h3>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3 text-xs">
          {settings.providers?.map((p: any) => (
            <div key={p.provider_id} className="p-4 rounded-xl bg-slate-50 border border-slate-200 space-y-1.5">
              <div className="flex items-center justify-between">
                <span className="font-bold text-slate-900">{p.name}</span>
                {p.provider_id === 'gemini' && p.configured ? (
                  <span className="inline-flex items-center gap-1 px-2 py-0.5 rounded-full text-[10px] font-bold bg-emerald-100 text-emerald-800 border border-emerald-300">
                    <CheckCircle2 className="w-3 h-3" /> Live API Active
                  </span>
                ) : p.provider_id === 'chatgpt' && p.configured ? (
                  <span className="inline-flex items-center gap-1 px-2 py-0.5 rounded-full text-[10px] font-bold bg-amber-100 text-amber-800 border border-amber-300" title="Key loaded in .env; prepaid balance is $0.00">
                    <CheckCircle2 className="w-3 h-3" /> Key Set (Manual Ingestion Active)
                  </span>
                ) : (
                  <span className="inline-flex items-center gap-1 px-2 py-0.5 rounded-full text-[10px] font-bold bg-cyan-100 text-cyan-800 border border-cyan-300">
                    <CheckCircle2 className="w-3 h-3" /> Built-in Research Active
                  </span>
                )}
              </div>
              <p className="font-mono text-[11px] text-slate-600">
                Adapter ID: <code>{p.provider_id}</code> · Model: <code>{p.default_model}</code>
              </p>
              <p className="text-[11px] text-slate-500">
                Env Variable(s): <code>{p.required_env_keys.join(' / ')}</code>
              </p>
              <p className="text-[11px] text-slate-500">
                Est. Cost / Query: <strong className="font-mono">${p.cost_per_call_usd}</strong>
              </p>
            </div>
          ))}
        </div>
      </div>

      {/* Windows Task Scheduler & CLI Guide */}
      <div className="bg-white rounded-xl border border-slate-200 p-5 shadow-2xs space-y-3">
        <h3 className="text-sm font-bold text-slate-900 flex items-center gap-2">
          <Terminal className="w-4 h-4 text-indigo-600" />
          CLI Commands & Windows Task Scheduler Weekly Automation Guide
        </h3>
        <p className="text-xs text-slate-600">
          Use the following PowerShell command to register a weekly scheduled task on Windows that refreshes multi-market observations,
          runs technical audit checks, and generates the weekly Markdown report without duplicating records:
        </p>
        <pre className="p-4 rounded-xl bg-slate-900 text-slate-100 font-mono text-xs overflow-x-auto">
{`# 1. Single CLI Command to Initialize, Audit, and Export Everything:
python -m engine.cli init --live-audit

# 2. Run Key-Free Test Mode Visibility Check (No Paid Keys Required):
python -m engine.cli run-visibility --mode test --markets US,IN,GB --limit 15

# 3. Register Weekly Windows Scheduled Task (Every Monday at 08:00 AM):
$Action = New-ScheduledTaskAction -Execute "python" -Argument "-m engine.cli run-visibility --mode live --markets US,IN,GB --limit 100" -WorkingDirectory "d:\\incubrix2"
$Trigger = New-ScheduledTaskTrigger -Weekly -DaysOfWeek Monday -At 8am
Register-ScheduledTask -TaskName "IncuBrix-Weekly-Visibility-Engine" -Action $Action -Trigger $Trigger -Description "Weekly AEO/SEO/GEO multi-market visibility run and report generation"`}
        </pre>
      </div>

      {/* Engine Run Audit Log */}
      <div className="bg-white rounded-xl border border-slate-200 p-5 shadow-2xs space-y-3">
        <h3 className="text-sm font-bold text-slate-900 flex items-center gap-2">
          <Clock className="w-4 h-4 text-emerald-600" />
          Engine Execution Run History & Audit Trail
        </h3>
        <div
          tabIndex={0}
          role="region"
          aria-label="Engine execution run logs"
          className="table-wrapper max-h-72"
        >
          <table>
            <thead>
              <tr className="border-b border-slate-200 text-left text-[11px] font-bold uppercase tracking-wider text-slate-500">
                <th className="py-2.5 px-4">Run ID</th>
                <th className="py-2.5 px-3">Type & Mode</th>
                <th className="py-2.5 px-3">Status</th>
                <th className="py-2.5 px-3">Observations (Verified / Skipped / Failed)</th>
                <th className="py-2.5 px-3">Duration & Cost</th>
                <th className="py-2.5 px-4">Started At</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-200 text-xs">
              {settings.runs?.map((r: any) => (
                <tr key={r.run_id} className="hover:bg-slate-50">
                  <th scope="row" className="py-2.5 px-4 font-mono font-bold text-slate-900 text-left">
                    {r.run_id}
                  </th>
                  <td className="py-2.5 px-3">
                    <span className="font-semibold text-slate-800">{r.run_type}</span>
                    <span className="block text-[11px] font-mono text-slate-500">mode: {r.mode}</span>
                  </td>
                  <td className="py-2.5 px-3">
                    <span className="px-2 py-0.5 rounded-full text-[11px] font-semibold bg-emerald-100 text-emerald-800">
                      {r.status}
                    </span>
                  </td>
                  <td className="py-2.5 px-3 font-mono">
                    Total: {r.observations_recorded} (
                    <span className="text-emerald-700 font-bold">{r.verified_count} ok</span> /{' '}
                    <span className="text-slate-500">{r.skipped_unavailable_count} unavail</span> /{' '}
                    <span className="text-rose-700">{r.failed_count} err</span>)
                  </td>
                  <td className="py-2.5 px-3 font-mono">
                    {r.duration_ms}ms · ${Number(r.estimated_cost_usd || 0).toFixed(4)}
                  </td>
                  <td className="py-2.5 px-4 font-mono text-[11px] text-slate-500">{r.started_at}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};
