import React, { useState, useEffect } from 'react';
import { Calendar, CheckCircle2, Clock, ShieldAlert, DollarSign } from 'lucide-react';

export const LaunchPlanSection: React.FC = () => {
  const [tasks, setTasks] = useState<any[]>([]);
  const [phaseFilter, setPhaseFilter] = useState('all');

  const loadTasks = async () => {
    const res = await fetch('/api/launch-plan');
    const data = await res.json();
    setTasks(data.tasks || []);
  };

  useEffect(() => {
    loadTasks();
  }, []);

  const handleStatusChange = async (taskId: string, newStatus: string) => {
    await fetch(`/api/launch-plan/${taskId}`, {
      method: 'PATCH',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ status: newStatus }),
    });
    await loadTasks();
  };

  const phases = Array.from(new Set(tasks.map((t) => t.phase)));
  const filtered = phaseFilter === 'all' ? tasks : tasks.filter((t) => t.phase === phaseFilter);
  const totalBudget = tasks.reduce((acc, t) => acc + Number(t.estimated_budget_usd || 0), 0);

  return (
    <div className="space-y-6" data-testid="launch-section">
      {/* Header */}
      <div className="bg-white rounded-xl border border-slate-200 p-5 shadow-2xs flex flex-col lg:flex-row lg:items-center justify-between gap-4">
        <div>
          <h2 className="text-lg font-bold text-slate-900">
            90-Day AEO / SEO / GEO Launch Plan (Weeks 1–12 Roadmap)
          </h2>
          <p className="text-xs text-slate-600 mt-1">
            Strictly separates <strong>Baseline Values</strong>, <strong>Proposed Targets</strong>, and{' '}
            <strong>Measured Results</strong> (never presenting a target as an achieved outcome).
          </p>
        </div>
        <div className="flex items-center gap-3">
          <div className="px-3 py-1.5 rounded-lg bg-slate-100 border border-slate-200 text-xs">
            Est. 90-Day Budget: <strong className="font-mono text-slate-900">${totalBudget.toFixed(0)} USD</strong>
          </div>
          <select
            aria-label="Filter by 30-day phase"
            value={phaseFilter}
            onChange={(e) => setPhaseFilter(e.target.value)}
            className="px-3 py-1.5 text-xs bg-slate-50 border border-slate-300 rounded-lg"
          >
            <option value="all">All 3 Phases (Days 1–90)</option>
            {phases.map((p) => (
              <option key={p} value={p}>
                {p}
              </option>
            ))}
          </select>
        </div>
      </div>

      {/* 12-Week Cards */}
      <div className="grid grid-cols-1 gap-4">
        {filtered.map((t) => (
          <div
            key={t.task_id}
            className="bg-white rounded-xl border border-slate-200 p-5 shadow-2xs space-y-3"
          >
            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 border-b border-slate-200 pb-3">
              <div className="flex items-center gap-2 flex-wrap">
                <span className="px-2.5 py-0.5 rounded bg-slate-900 text-white font-mono text-xs font-bold">
                  Week {t.week_number} ({t.task_id})
                </span>
                <span className="px-2.5 py-0.5 rounded bg-cyan-50 text-cyan-800 border border-cyan-200 text-xs font-semibold">
                  {t.phase}
                </span>
                <span className="text-xs text-slate-500">
                  Owner: <strong className="text-slate-800">{t.owner_role}</strong>
                </span>
              </div>
              <div className="flex items-center gap-2">
                <span className="text-xs font-mono text-slate-600">
                  Budget: <strong>${t.estimated_budget_usd}</strong>
                </span>
                <select
                  aria-label={`Status for ${t.task_id}`}
                  value={t.status}
                  onChange={(e) => handleStatusChange(t.task_id, e.target.value)}
                  className={`px-2.5 py-1 rounded-full text-xs font-bold border cursor-pointer ${
                    t.status === 'completed'
                      ? 'bg-emerald-100 text-emerald-900 border-emerald-300'
                      : t.status === 'in_progress'
                      ? 'bg-amber-100 text-amber-900 border-amber-300'
                      : 'bg-slate-100 text-slate-700 border-slate-300'
                  }`}
                >
                  <option value="completed">Completed</option>
                  <option value="in_progress">In Progress</option>
                  <option value="planned">Planned</option>
                </select>
              </div>
            </div>

            <div>
              <h3 className="text-sm font-bold text-slate-900">{t.title}</h3>
              <p className="text-xs text-slate-600 mt-1 leading-relaxed">{t.description}</p>
            </div>

            {/* Explicit Separation: Baseline vs Proposed Target vs Measured Outcome */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-3 text-xs">
              <div className="p-3 rounded-lg bg-slate-50 border border-slate-200">
                <span className="text-[10px] font-bold uppercase tracking-wider text-slate-500 block">
                  1. Verified Baseline Value
                </span>
                <p className="text-slate-800 font-medium mt-1">{t.baseline_metric}</p>
              </div>
              <div className="p-3 rounded-lg bg-blue-50/60 border border-blue-200">
                <span className="text-[10px] font-bold uppercase tracking-wider text-blue-700 block">
                  2. Proposed 90-Day Target (Not Yet Claimed as Achieved)
                </span>
                <p className="text-blue-950 font-medium mt-1">{t.target_metric}</p>
              </div>
              <div className="p-3 rounded-lg bg-emerald-50/70 border border-emerald-200">
                <span className="text-[10px] font-bold uppercase tracking-wider text-emerald-800 block">
                  3. Actual Measured Outcome to Date
                </span>
                <p className="text-emerald-950 font-semibold mt-1">{t.measured_metric}</p>
              </div>
            </div>

            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 pt-2 border-t border-slate-100 text-[11px] text-slate-500">
              <span>
                <strong>Tools:</strong> {t.tools_used} · <strong>Dependencies:</strong> {t.dependencies}
              </span>
              <span className="text-amber-800">
                <strong>Risk & Mitigation:</strong> {t.risk_and_mitigation}
              </span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};
