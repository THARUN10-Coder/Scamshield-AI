import React, { useState, useEffect } from 'react';
import { apiService } from '../services/api';
import { ScanRecord } from '../types';
import { RiskBadge } from '../components/RiskBadge';
import { Trash2, Loader2 } from 'lucide-react';

interface HistoryViewProps {
  onViewDetails: (scan: ScanRecord) => void;
}

export const HistoryView: React.FC<HistoryViewProps> = ({ onViewDetails }) => {
  const [scans, setScans] = useState<ScanRecord[]>([]);
  const [loading, setLoading] = useState(true);
  const [riskFilter, setRiskFilter] = useState('ALL');
  const [typeFilter, setTypeFilter] = useState('ALL');
  const [searchQuery, setSearchQuery] = useState('');

  const loadHistory = async () => {
    setLoading(true);
    try {
      const data = await apiService.getScans({
        risk_level: riskFilter !== 'ALL' ? riskFilter : undefined,
        scan_type: typeFilter !== 'ALL' ? typeFilter : undefined,
      });
      setScans(data);
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadHistory();
  }, [riskFilter, typeFilter]);

  const handleDelete = async (id: string, e: React.MouseEvent) => {
    e.stopPropagation();
    if (!confirm('Are you sure you want to remove this scan from your history?')) return;
    try {
      await apiService.deleteScan(id);
      setScans(scans.filter((s) => s.id !== id));
    } catch (e) {
      alert('Failed to delete scan record');
    }
  };

  const filteredScans = scans.filter((s) => {
    if (!searchQuery) return true;
    return (
      s.explanation.toLowerCase().includes(searchQuery.toLowerCase()) ||
      s.scan_type.toLowerCase().includes(searchQuery.toLowerCase()) ||
      s.recommendation.toLowerCase().includes(searchQuery.toLowerCase())
    );
  });

  return (
    <div className="space-y-6">
      {/* Header & Filters */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 glass-panel bg-card border border-border p-6 rounded-2xl">
        <div>
          <h2 className="text-xl font-bold text-white tracking-tight">Scan History & Audit Log</h2>
          <p className="text-xs text-muted-foreground">All submitted evaluations stored securely with hashed inputs</p>
        </div>

        <div className="flex flex-wrap items-center gap-3">
          {/* Risk Level Filter */}
          <div className="flex items-center gap-1.5 bg-secondary p-1 rounded-lg border border-border text-xs">
            {['ALL', 'HIGH', 'MEDIUM', 'LOW'].map((lvl) => (
              <button
                key={lvl}
                onClick={() => setRiskFilter(lvl)}
                className={`px-3 py-1.5 rounded-md transition font-medium ${
                  riskFilter === lvl
                    ? 'bg-primary text-primary-foreground font-bold'
                    : 'text-muted-foreground hover:text-white'
                }`}
              >
                {lvl}
              </button>
            ))}
          </div>

          {/* Type Filter */}
          <select
            value={typeFilter}
            onChange={(e) => setTypeFilter(e.target.value)}
            className="bg-secondary border border-border rounded-lg px-3 py-2 text-xs text-slate-200 focus:outline-none focus:border-primary"
          >
            <option value="ALL">All Vectors</option>
            <option value="message">Message</option>
            <option value="url">URL</option>
            <option value="qr">QR Code</option>
            <option value="phone">Phone</option>
            <option value="payment">Payment</option>
            <option value="screenshot">Screenshot</option>
          </select>
        </div>
      </div>

      {/* History Records List */}
      <div className="glass-panel bg-card border border-border rounded-2xl p-6">
        {loading ? (
          <div className="flex items-center justify-center py-16 text-muted-foreground">
            <Loader2 className="w-6 h-6 animate-spin text-primary" />
            <span className="ml-2 text-sm">Loading scan records...</span>
          </div>
        ) : filteredScans.length === 0 ? (
          <div className="text-center py-16 text-muted-foreground italic text-sm">
            No scan records matched your selected criteria.
          </div>
        ) : (
          <div className="space-y-3">
            {filteredScans.map((scan) => (
              <div
                key={scan.id}
                onClick={() => onViewDetails(scan)}
                className="p-4 rounded-xl bg-secondary border border-border hover:border-border-light transition flex flex-col md:flex-row md:items-center justify-between gap-4 cursor-pointer group"
              >
                <div className="space-y-1.5 flex-1">
                  <div className="flex items-center gap-2">
                    <span className="text-xs font-bold uppercase tracking-wider text-primary">
                      {scan.scan_type}
                    </span>
                    <span className="text-xs text-muted-foreground">•</span>
                    <span className="text-xs text-muted-foreground">
                      {new Date(scan.created_at).toLocaleString()}
                    </span>
                    <RiskBadge level={scan.risk_level} size="sm" />
                  </div>
                  <p className="text-sm font-medium text-slate-200 line-clamp-1">
                    {scan.explanation}
                  </p>
                  <p className="text-xs text-muted-foreground line-clamp-1">
                    Rec: {scan.recommendation}
                  </p>
                </div>

                <div className="flex items-center gap-4">
                  <div className="text-right">
                    <span className="text-xl font-bold font-mono text-white">
                      {scan.risk_score}
                    </span>
                    <span className="text-xs text-muted-foreground">/100</span>
                  </div>

                  <button
                    onClick={(e) => handleDelete(scan.id, e)}
                    className="p-2 rounded-lg bg-card text-muted-foreground hover:text-destructive hover:bg-muted transition"
                    title="Delete record"
                  >
                    <Trash2 className="w-4 h-4" />
                  </button>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};
