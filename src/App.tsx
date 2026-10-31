import React, { useState, useEffect, useCallback } from 'react';
import {
  LayoutDashboard,
  Eye,
  ShieldCheck,
  FileText,
  Award,
  HelpCircle,
  FileBarChart2,
  Rocket,
  Settings,
  Globe,
  ExternalLink,
  Menu,
  X,
} from 'lucide-react';
import { OverviewMetrics, SectionId } from './types';
import { OverviewSection } from './components/OverviewSection';
import { VisibilitySection } from './components/VisibilitySection';
import { AuditSection } from './components/AuditSection';
import { ContentStudioSection } from './components/ContentStudioSection';
import { CitationsSection } from './components/CitationsSection';
import { QuestionsSection } from './components/QuestionsSection';
import { ReportsSection } from './components/ReportsSection';
import { LaunchPlanSection } from './components/LaunchPlanSection';
import { SettingsSection } from './components/SettingsSection';

const NAV_ITEMS: Array<{
  id: SectionId;
  label: string;
  badge?: string;
  icon: React.FC<{ className?: string }>;
}> = [
  { id: 'overview', label: 'Overview', icon: LayoutDashboard },
  { id: 'visibility', label: 'Visibility Tracker', badge: '5 Providers', icon: Eye },
  { id: 'audit', label: 'Technical SEO Audit', badge: '22 Fixes', icon: ShieldCheck },
  { id: 'content', label: 'Content Studio', badge: '10 Pages', icon: FileText },
  { id: 'citations', label: 'Citation Opportunities', badge: '30 URLs', icon: Award },
  { id: 'questions', label: 'Research Questions', badge: '100', icon: HelpCircle },
  { id: 'reports', label: 'Reports', icon: FileBarChart2 },
  { id: 'launch', label: 'Launch Plan', badge: '90-Day', icon: Rocket },
  { id: 'settings', label: 'Settings & Data Sources', icon: Settings },
];

export const App: React.FC = () => {
  const [activeSection, setActiveSection] = useState<SectionId>('overview');
  const [globalMarket, setGlobalMarket] = useState<string>('all');
  const [metrics, setMetrics] = useState<OverviewMetrics | null>(null);
  const [loadingOverview, setLoadingOverview] = useState<boolean>(true);
  const [mobileMenuOpen, setMobileMenuOpen] = useState<boolean>(false);

  const fetchOverview = useCallback(async () => {
    setLoadingOverview(true);
    try {
      const res = await fetch('/api/overview');
      const data = await res.json();
      setMetrics(data);
    } finally {
      setLoadingOverview(false);
    }
  }, []);

  useEffect(() => {
    fetchOverview();
  }, [fetchOverview]);

  return (
    <div className="min-h-screen flex bg-[#F8FAFC] text-[#0F172A]">
      {/* Persistent Desktop Sidebar */}
      <aside
        aria-label="Primary Module Navigation"
        className="hidden lg:flex flex-col w-68 bg-white border-r border-slate-200 shrink-0 sticky top-0 h-screen"
      >
        <div className="p-5 border-b border-slate-200">
          <div className="flex items-center gap-2.5">
            <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-cyan-600 to-blue-700 flex items-center justify-center text-white font-extrabold text-sm shadow-xs">
              IB
            </div>
            <div>
              <h1 className="text-sm font-extrabold text-slate-900 tracking-tight">
                IncuBrix Visibility
              </h1>
              <p className="text-[11px] font-medium text-cyan-700">
                AEO · SEO · GEO Engine
              </p>
            </div>
          </div>
          <div className="mt-3 p-2.5 rounded-lg bg-slate-50 border border-slate-200/80 text-[11px]">
            <div className="flex items-center justify-between text-slate-500">
              <span>Assessment Target</span>
              <span className="px-1.5 py-0.2 rounded bg-emerald-100 text-emerald-800 font-bold text-[10px]">
                LIVE AUDIT
              </span>
            </div>
            <a
              href="https://www.incubrix.com"
              target="_blank"
              rel="noreferrer"
              className="font-mono font-semibold text-slate-800 hover:text-cyan-700 inline-flex items-center gap-1 mt-0.5"
            >
              https://www.incubrix.com
              <ExternalLink className="w-3 h-3" />
            </a>
          </div>
        </div>

        <nav className="flex-1 p-3 space-y-1 overflow-y-auto">
          {NAV_ITEMS.map((item) => {
            const Icon = item.icon;
            const active = activeSection === item.id;
            return (
              <button
                key={item.id}
                data-testid={`nav-${item.id}`}
                onClick={() => setActiveSection(item.id)}
                className={`w-full flex items-center justify-between px-3 py-2.5 rounded-lg text-xs font-semibold transition cursor-pointer ${
                  active
                    ? 'bg-cyan-50 text-cyan-900 border border-cyan-200/80 shadow-2xs'
                    : 'text-slate-600 hover:bg-slate-100 hover:text-slate-900'
                }`}
              >
                <span className="flex items-center gap-2.5">
                  <Icon className={`w-4 h-4 ${active ? 'text-cyan-600' : 'text-slate-400'}`} />
                  {item.label}
                </span>
                {item.badge && (
                  <span
                    className={`px-1.5 py-0.5 rounded text-[10px] font-mono font-bold ${
                      active ? 'bg-cyan-600 text-white' : 'bg-slate-100 text-slate-600'
                    }`}
                  >
                    {item.badge}
                  </span>
                )}
              </button>
            );
          })}
        </nav>

        <div className="p-4 border-t border-slate-200 bg-slate-50/60 text-[11px] text-slate-500 space-y-1">
          <p className="font-semibold text-slate-700">Evidence Integrity Mode</p>
          <p>SQLite: <code className="text-slate-800">data/incubrix.db</code></p>
          <p>Zero fabricated live rankings</p>
        </div>
      </aside>

      {/* Main Content Area */}
      <div className="flex-1 flex flex-col min-w-0">
        {/* Top Navigation Bar */}
        <header className="sticky top-0 z-30 bg-white/95 backdrop-blur border-b border-slate-200 px-4 lg:px-8 py-3 flex items-center justify-between gap-4">
          <div className="flex items-center gap-3">
            <button
              onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
              className="lg:hidden p-2 rounded-lg border border-slate-200 text-slate-700"
              aria-label="Toggle navigation menu"
            >
              {mobileMenuOpen ? <X className="w-5 h-5" /> : <Menu className="w-5 h-5" />}
            </button>
            <div>
              <h2 className="text-sm sm:text-base font-extrabold text-slate-900">
                {NAV_ITEMS.find((i) => i.id === activeSection)?.label}
              </h2>
              <p className="text-[11px] text-slate-500 hidden sm:block">
                IncuBrix Growth Engineer Assessment — Option 3: AEO, SEO & GEO Visibility Engine
              </p>
            </div>
          </div>

          {/* Global Market Context Selector */}
          <div className="flex items-center gap-3">
            <div className="flex items-center gap-1.5 bg-slate-100 border border-slate-200 rounded-lg px-2.5 py-1">
              <Globe className="w-3.5 h-3.5 text-cyan-600" />
              <label htmlFor="global-market-select" className="text-[11px] font-semibold text-slate-600">
                Market:
              </label>
              <select
                id="global-market-select"
                value={globalMarket}
                onChange={(e) => setGlobalMarket(e.target.value)}
                className="text-xs font-bold text-slate-900 bg-transparent focus:outline-none cursor-pointer"
              >
                <option value="all">All Markets (US, IN, GB)</option>
                <option value="US">United States (en-US)</option>
                <option value="IN">India (en-IN)</option>
                <option value="GB">United Kingdom (en-GB)</option>
              </select>
            </div>
          </div>
        </header>

        {/* Mobile Drawer Navigation */}
        {mobileMenuOpen && (
          <div className="lg:hidden bg-white border-b border-slate-200 p-3 space-y-1">
            {NAV_ITEMS.map((item) => {
              const Icon = item.icon;
              return (
                <button
                  key={item.id}
                  onClick={() => {
                    setActiveSection(item.id);
                    setMobileMenuOpen(false);
                  }}
                  className={`w-full flex items-center justify-between px-3 py-2 rounded-lg text-xs font-semibold ${
                    activeSection === item.id ? 'bg-cyan-50 text-cyan-900' : 'text-slate-600'
                  }`}
                >
                  <span className="flex items-center gap-2">
                    <Icon className="w-4 h-4" />
                    {item.label}
                  </span>
                  {item.badge && <span className="text-[10px] font-mono">{item.badge}</span>}
                </button>
              );
            })}
          </div>
        )}

        {/* Active Module Workspace */}
        <main className="flex-1 p-4 lg:p-8 max-w-[1440px] w-full mx-auto">
          {activeSection === 'overview' && (
            <OverviewSection
              metrics={metrics}
              loading={loadingOverview}
              onNavigate={setActiveSection}
              onRefresh={fetchOverview}
            />
          )}
          {activeSection === 'visibility' && (
            <VisibilitySection globalMarket={globalMarket} onDataChanged={fetchOverview} />
          )}
          {activeSection === 'audit' && <AuditSection onDataChanged={fetchOverview} />}
          {activeSection === 'content' && <ContentStudioSection onDataChanged={fetchOverview} />}
          {activeSection === 'citations' && <CitationsSection />}
          {activeSection === 'questions' && <QuestionsSection onDataChanged={fetchOverview} />}
          {activeSection === 'reports' && <ReportsSection />}
          {activeSection === 'launch' && <LaunchPlanSection />}
          {activeSection === 'settings' && <SettingsSection />}
        </main>
      </div>
    </div>
  );
};
