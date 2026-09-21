import React, { useState, useEffect } from 'react';
import {
  Shield,
  LayoutDashboard,
  Search,
  History,
  Flag,
  BookOpen,
  Menu,
  X,
  User,
  Sparkles,
  Zap
} from 'lucide-react';
import { DashboardView } from './pages/DashboardView';
import { ScanCenter } from './components/ScanCenter';
import { HistoryView } from './pages/HistoryView';
import { ReportView } from './pages/ReportView';
import { SafetyCenterView } from './pages/SafetyCenterView';
import { RiskResultModal } from './components/RiskResultModal';
import { apiService } from './services/api';
import { ScanResult, StatisticsResponse, ScanRecord } from './types';

export function App() {
  const [currentTab, setCurrentTab] = useState<'dashboard' | 'scan' | 'history' | 'reports' | 'safety'>('dashboard');
  const [activeModalResult, setActiveModalResult] = useState<ScanResult | null>(null);
  const [stats, setStats] = useState<StatisticsResponse | null>(null);
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  // Fetch stats for dashboard
  const refreshStats = async () => {
    try {
      const data = await apiService.getStatistics();
      setStats(data);
    } catch (e) {
      console.error('Error fetching statistics:', e);
    }
  };

  useEffect(() => {
    refreshStats();
  }, [currentTab]);

  const handleScanCompleted = (res: ScanResult) => {
    setActiveModalResult(res);
    refreshStats();
  };

  const handleInspectRecord = (record: ScanRecord) => {
    setActiveModalResult({
      scan_id: record.id,
      scan_type: record.scan_type,
      risk_score: record.risk_score,
      risk_level: record.risk_level,
      confidence: record.confidence as any,
      indicators: record.indicators,
      explanation: record.explanation,
      recommendation: record.recommendation,
    });
  };

  const navItems = [
    { id: 'dashboard', label: 'Dashboard', icon: LayoutDashboard },
    { id: 'scan', label: 'Scan Center', icon: Search, badge: 'Active' },
    { id: 'history', label: 'Audit History', icon: History },
    { id: 'reports', label: 'Report Scam', icon: Flag },
    { id: 'safety', label: 'Safety Center', icon: BookOpen },
  ];

  return (
    <div className="min-h-screen flex flex-col md:flex-row bg-background text-slate-100 selection:bg-primary selection:text-primary-foreground">
      {/* Sidebar for Desktop (baroworks theme) */}
      <aside className="hidden md:flex flex-col w-64 bg-card border-r border-border p-5 space-y-8 flex-shrink-0 z-20">
        {/* Brand Header */}
        <div className="flex items-center gap-3 px-2">
          <div className="w-10 h-10 rounded-xl bg-primary flex items-center justify-center text-primary-foreground font-black shadow-lg shadow-primary/20">
            <Shield className="w-5 h-5 text-primary-foreground" />
          </div>
          <div>
            <h1 className="text-base font-extrabold tracking-tight text-white flex items-center gap-1">
              SCAMSHIELD<span className="text-primary">AI</span>
            </h1>
            <p className="text-[10px] uppercase tracking-wider text-muted-foreground font-semibold">
              baroworks dark theme
            </p>
          </div>
        </div>

        {/* Navigation links */}
        <nav className="space-y-1 flex-1">
          {navItems.map((item) => {
            const Icon = item.icon;
            const active = currentTab === item.id;
            return (
              <button
                key={item.id}
                onClick={() => setCurrentTab(item.id as any)}
                className={`w-full flex items-center justify-between px-3.5 py-2.5 rounded-lg text-xs font-semibold transition-all ${
                  active
                    ? 'bg-secondary text-primary border border-border shadow-sm'
                    : 'text-muted-foreground hover:text-white hover:bg-secondary/60'
                }`}
              >
                <div className="flex items-center gap-3">
                  <Icon className={`w-4 h-4 ${active ? 'text-primary' : 'text-muted-foreground'}`} />
                  <span>{item.label}</span>
                </div>
                {item.badge && (
                  <span className="px-2 py-0.5 rounded text-[10px] bg-primary/15 text-primary font-bold">
                    {item.badge}
                  </span>
                )}
              </button>
            );
          })}
        </nav>

        {/* Hackathon Presentation Info Banner */}
        <div className="p-4 rounded-xl bg-secondary border border-border space-y-2 text-xs">
          <div className="flex items-center gap-2 text-primary font-semibold">
            <Zap className="w-3.5 h-3.5" />
            <span>Hackathon / Demo Mode</span>
          </div>
          <p className="text-[11px] text-muted-foreground leading-relaxed">
            Multi-signal AI engine evaluating SMS, Phishing URLs, UPI QR payloads, and Coercive context.
          </p>
        </div>
      </aside>

      {/* Main Content Area */}
      <div className="flex-1 flex flex-col min-w-0">
        {/* Top Navbar */}
        <header className="h-16 border-b border-border px-6 flex items-center justify-between bg-card/80 backdrop-blur-md sticky top-0 z-30">
          <div className="flex items-center gap-3 md:hidden">
            <button
              onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
              className="p-2 rounded-lg bg-secondary text-slate-300"
            >
              {mobileMenuOpen ? <X className="w-5 h-5" /> : <Menu className="w-5 h-5" />}
            </button>
            <div className="flex items-center gap-2">
              <div className="w-6 h-6 rounded bg-primary flex items-center justify-center">
                <Shield className="w-4 h-4 text-primary-foreground" />
              </div>
              <span className="font-bold text-white text-sm">ScamShield AI</span>
            </div>
          </div>

          <div className="hidden md:flex items-center gap-2 text-xs text-muted-foreground">
            <span>Platform Status:</span>
            <span className="inline-flex items-center gap-1.5 text-success font-semibold">
              <span className="w-1.5 h-1.5 rounded-full bg-success"></span>
              AI Detection Pipeline Online (v1.0)
            </span>
          </div>

          <div className="flex items-center gap-3">
            <button
              onClick={() => setCurrentTab('scan')}
              className="hidden sm:flex items-center gap-2 px-4 py-2 rounded-lg bg-primary hover:bg-primary-hover text-primary-foreground font-bold text-xs transition shadow-sm"
            >
              <Sparkles className="w-3.5 h-3.5" />
              <span>Quick Scan</span>
            </button>
            <div className="w-9 h-9 rounded-lg bg-secondary border border-border flex items-center justify-center text-muted-foreground hover:text-white transition">
              <User className="w-4 h-4" />
            </div>
          </div>
        </header>

        {/* Mobile Navigation Drawer */}
        {mobileMenuOpen && (
          <div className="md:hidden glass-panel border-b border-border p-4 space-y-1 z-40 bg-card">
            {navItems.map((item) => {
              const Icon = item.icon;
              return (
                <button
                  key={item.id}
                  onClick={() => {
                    setCurrentTab(item.id as any);
                    setMobileMenuOpen(false);
                  }}
                  className={`w-full flex items-center gap-3 px-4 py-2.5 rounded-lg text-xs font-semibold ${
                    currentTab === item.id
                      ? 'bg-secondary text-primary font-bold border border-border'
                      : 'text-muted-foreground hover:text-white'
                  }`}
                >
                  <Icon className="w-4 h-4" />
                  <span>{item.label}</span>
                </button>
              );
            })}
          </div>
        )}

        {/* Page Views Container */}
        <main className="p-4 sm:p-6 md:p-8 max-w-7xl mx-auto w-full space-y-6 flex-1">
          {currentTab === 'dashboard' && (
            <DashboardView
              stats={stats}
              onNavigateToScan={() => setCurrentTab('scan')}
              onViewScan={handleInspectRecord}
            />
          )}

          {currentTab === 'scan' && (
            <ScanCenter onScanComplete={handleScanCompleted} />
          )}

          {currentTab === 'history' && (
            <HistoryView onViewDetails={handleInspectRecord} />
          )}

          {currentTab === 'reports' && <ReportView />}

          {currentTab === 'safety' && <SafetyCenterView />}
        </main>

        {/* Modal for explainable assessment result */}
        <RiskResultModal
          result={activeModalResult}
          onClose={() => setActiveModalResult(null)}
        />
      </div>
    </div>
  );
}
export default App;
