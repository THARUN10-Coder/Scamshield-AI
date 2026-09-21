import React from 'react';
import { ScanRecord, StatisticsResponse } from '../types';
import { RiskBadge } from '../components/RiskBadge';
import {
  ShieldAlert,
  ShieldCheck,
  AlertTriangle,
  Activity,
  ArrowRight,
  TrendingUp,
  Clock
} from 'lucide-react';
import {
  PieChart,
  Pie,
  Cell,
  ResponsiveContainer,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip
} from 'recharts';

interface DashboardViewProps {
  stats: StatisticsResponse | null;
  onNavigateToScan: () => void;
  onViewScan: (scan: ScanRecord) => void;
}

export const DashboardView: React.FC<DashboardViewProps> = ({
  stats,
  onNavigateToScan,
  onViewScan,
}) => {
  const pieData = stats
    ? [
        { name: 'High Risk', value: stats.high_risk_count, color: '#FF5C67' },
        { name: 'Medium Risk', value: stats.medium_risk_count, color: '#F5BE38' },
        { name: 'Low Risk', value: stats.low_risk_count, color: '#3DD68C' },
      ].filter((d) => d.value > 0)
    : [];

  const barData = stats
    ? Object.entries(stats.scans_by_type).map(([type, count]) => ({
        type: type.toUpperCase(),
        count,
      }))
    : [];

  return (
    <div className="space-y-6">
      {/* Top Welcome & Quick Action Card */}
      <div className="p-6 md:p-8 rounded-2xl glass-panel bg-card border border-border relative overflow-hidden flex flex-col md:flex-row items-start md:items-center justify-between gap-6">
        <div className="space-y-2 max-w-xl z-10">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-primary/15 text-primary border border-primary/30 text-xs font-semibold">
            <span className="w-2 h-2 rounded-full bg-primary animate-pulse"></span>
            Pre-Transaction Fraud Defense Active
          </div>
          <h2 className="text-2xl md:text-3xl font-extrabold text-white tracking-tight">
            Stop Scams Before You Pay
          </h2>
          <p className="text-sm text-muted-foreground leading-relaxed">
            Analyze suspicious messages, links, payment requests, and QR codes before authorizing transactions.
          </p>
        </div>
        <button
          onClick={onNavigateToScan}
          className="z-10 flex items-center gap-2 px-6 py-3 rounded-lg bg-primary hover:bg-primary-hover text-primary-foreground font-bold text-sm shadow-lg shadow-primary/10 transition group"
        >
          <span>Scan Something Suspicious</span>
          <ArrowRight className="w-4 h-4 group-hover:translate-x-1 transition-transform" />
        </button>
      </div>

      {/* Metric Cards Grid */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <div className="p-5 rounded-xl glass-card bg-card border border-border space-y-2">
          <div className="flex items-center justify-between text-muted-foreground">
            <span className="text-xs font-semibold uppercase tracking-wider">Total Scans</span>
            <Activity className="w-4 h-4 text-primary" />
          </div>
          <p className="text-3xl font-extrabold text-white">{stats?.total_scans ?? 0}</p>
          <p className="text-xs text-muted-foreground">Pre-transaction evaluations</p>
        </div>

        <div className="p-5 rounded-xl glass-card bg-card border border-destructive/20 space-y-2">
          <div className="flex items-center justify-between text-destructive">
            <span className="text-xs font-semibold uppercase tracking-wider">High Risk</span>
            <ShieldAlert className="w-4 h-4 text-destructive" />
          </div>
          <p className="text-3xl font-extrabold text-destructive">{stats?.high_risk_count ?? 0}</p>
          <p className="text-xs text-muted-foreground">Critical threats intercepted</p>
        </div>

        <div className="p-5 rounded-xl glass-card bg-card border border-primary/20 space-y-2">
          <div className="flex items-center justify-between text-primary">
            <span className="text-xs font-semibold uppercase tracking-wider">Medium Risk</span>
            <AlertTriangle className="w-4 h-4 text-primary" />
          </div>
          <p className="text-3xl font-extrabold text-primary">{stats?.medium_risk_count ?? 0}</p>
          <p className="text-xs text-muted-foreground">Anomalous / suspicious patterns</p>
        </div>

        <div className="p-5 rounded-xl glass-card bg-card border border-success/20 space-y-2">
          <div className="flex items-center justify-between text-success">
            <span className="text-xs font-semibold uppercase tracking-wider">Low Risk</span>
            <ShieldCheck className="w-4 h-4 text-success" />
          </div>
          <p className="text-3xl font-extrabold text-success">{stats?.low_risk_count ?? 0}</p>
          <p className="text-xs text-muted-foreground">Verified safe requests</p>
        </div>
      </div>

      {/* Visual Analytics Charts Section */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Risk Distribution Chart */}
        <div className="p-6 rounded-2xl glass-panel bg-card border border-border space-y-4">
          <div className="flex items-center justify-between">
            <h3 className="text-base font-bold text-white flex items-center gap-2">
              <TrendingUp className="w-4 h-4 text-primary" />
              <span>Risk Distribution</span>
            </h3>
            <span className="text-xs text-muted-foreground">Aggregated breakdown</span>
          </div>

          <div className="h-56 flex items-center justify-center">
            {pieData.length > 0 ? (
              <ResponsiveContainer width="100%" height="100%">
                <PieChart>
                  <Pie
                    data={pieData}
                    cx="50%"
                    cy="50%"
                    innerRadius={50}
                    outerRadius={75}
                    paddingAngle={6}
                    dataKey="value"
                  >
                    {pieData.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={entry.color} />
                    ))}
                  </Pie>
                  <Tooltip
                    contentStyle={{
                      backgroundColor: '#13141B',
                      borderColor: '#252733',
                      borderRadius: '8px',
                      color: '#fff',
                    }}
                  />
                </PieChart>
              </ResponsiveContainer>
            ) : (
              <p className="text-xs text-muted-foreground italic">No scan records recorded yet.</p>
            )}
          </div>
        </div>

        {/* Scans By Channel Chart */}
        <div className="p-6 rounded-2xl glass-panel bg-card border border-border space-y-4">
          <div className="flex items-center justify-between">
            <h3 className="text-base font-bold text-white flex items-center gap-2">
              <Activity className="w-4 h-4 text-primary" />
              <span>Scans by Vector</span>
            </h3>
            <span className="text-xs text-muted-foreground">Message / Link / QR / Phone</span>
          </div>

          <div className="h-56 flex items-center justify-center">
            {barData.length > 0 ? (
              <ResponsiveContainer width="100%" height="100%">
                <BarChart data={barData}>
                  <XAxis dataKey="type" stroke="#64748B" fontSize={11} tickLine={false} />
                  <YAxis stroke="#64748B" fontSize={11} tickLine={false} />
                  <Tooltip
                    contentStyle={{
                      backgroundColor: '#13141B',
                      borderColor: '#252733',
                      borderRadius: '8px',
                      color: '#fff',
                    }}
                  />
                  <Bar dataKey="count" fill="#F5BE38" radius={[4, 4, 0, 0]} />
                </BarChart>
              </ResponsiveContainer>
            ) : (
              <p className="text-xs text-muted-foreground italic">No vector data available yet.</p>
            )}
          </div>
        </div>
      </div>

      {/* Recent Scans Table */}
      <div className="p-6 rounded-2xl glass-panel bg-card border border-border space-y-4">
        <div className="flex items-center justify-between">
          <h3 className="text-base font-bold text-white flex items-center gap-2">
            <Clock className="w-4 h-4 text-primary" />
            <span>Recent Evaluations</span>
          </h3>
        </div>

        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs">
            <thead className="text-muted-foreground uppercase border-b border-border tracking-wider">
              <tr>
                <th className="py-3 px-3">Vector</th>
                <th className="py-3 px-3">Score</th>
                <th className="py-3 px-3">Risk Level</th>
                <th className="py-3 px-3">Key Reason</th>
                <th className="py-3 px-3 text-right">Action</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-border text-slate-300">
              {stats && stats.recent_scans.length > 0 ? (
                stats.recent_scans.slice(0, 5).map((scan) => (
                  <tr key={scan.id} className="hover:bg-secondary transition">
                    <td className="py-3 px-3 font-semibold uppercase text-primary">
                      {scan.scan_type}
                    </td>
                    <td className="py-3 px-3 font-mono font-bold text-white">
                      {scan.risk_score}/100
                    </td>
                    <td className="py-3 px-3">
                      <RiskBadge level={scan.risk_level} size="sm" />
                    </td>
                    <td className="py-3 px-3 truncate max-w-xs text-muted-foreground">
                      {scan.explanation}
                    </td>
                    <td className="py-3 px-3 text-right">
                      <button
                        onClick={() => onViewScan(scan)}
                        className="px-3 py-1 rounded-md bg-secondary hover:bg-muted text-primary text-xs transition border border-border font-medium"
                      >
                        Inspect
                      </button>
                    </td>
                  </tr>
                ))
              ) : (
                <tr>
                  <td colSpan={5} className="py-8 text-center text-muted-foreground italic">
                    No scans evaluated yet. Click "Scan Something Suspicious" above to test.
                  </td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};
