import React from 'react';
import { RiskBadge } from './RiskBadge';
import { IndicatorDetail } from '../types';
import { AlertCircle, AlertOctagon, CheckCircle2, ShieldAlert, Sparkles } from 'lucide-react';

interface RiskResultModalProps {
  result: {
    risk_score: number;
    risk_level: 'LOW' | 'MEDIUM' | 'HIGH';
    confidence: 'low' | 'medium' | 'high';
    indicators: IndicatorDetail[];
    explanation: string;
    recommendation: string;
    extracted_metadata?: any;
  } | null;
  onClose: () => void;
}

export const RiskResultModal: React.FC<RiskResultModalProps> = ({ result, onClose }) => {
  if (!result) return null;

  const scoreColor =
    result.risk_level === 'HIGH'
      ? 'text-destructive'
      : result.risk_level === 'MEDIUM'
      ? 'text-primary'
      : 'text-success';

  const strokeColor =
    result.risk_level === 'HIGH'
      ? '#FF5C67'
      : result.risk_level === 'MEDIUM'
      ? '#F5BE38'
      : '#3DD68C';

  // Circular gauge calculations
  const radius = 54;
  const circumference = 2 * Math.PI * radius;
  const strokeDashoffset = circumference - (result.risk_score / 100) * circumference;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/85 backdrop-blur-md animate-in fade-in duration-200">
      <div className="relative w-full max-w-2xl max-h-[90vh] overflow-y-auto glass-panel rounded-2xl border border-border shadow-2xl p-6 md:p-8 space-y-6 bg-card">
        {/* Header */}
        <div className="flex items-center justify-between border-b border-border pb-4">
          <div className="flex items-center gap-3">
            <div className="p-2.5 rounded-xl bg-secondary border border-border">
              <Sparkles className="w-5 h-5 text-primary" />
            </div>
            <div>
              <h3 className="text-xl font-bold text-white tracking-tight">AI Pre-Transaction Risk Assessment</h3>
              <p className="text-xs text-muted-foreground">Explainable multi-signal fraud evaluation</p>
            </div>
          </div>
          <button
            onClick={onClose}
            className="text-muted-foreground hover:text-white p-2 rounded-lg bg-secondary hover:bg-muted transition"
          >
            ✕
          </button>
        </div>

        {/* Score & Gauge Section */}
        <div className="flex flex-col sm:flex-row items-center gap-6 p-6 rounded-xl bg-secondary border border-border">
          <div className="relative w-32 h-32 flex-shrink-0 flex items-center justify-center">
            <svg className="w-full h-full transform -rotate-90">
              <circle
                cx="64"
                cy="64"
                r={radius}
                stroke="#252733"
                strokeWidth="10"
                fill="transparent"
              />
              <circle
                cx="64"
                cy="64"
                r={radius}
                stroke={strokeColor}
                strokeWidth="10"
                strokeDasharray={circumference}
                strokeDashoffset={strokeDashoffset}
                strokeLinecap="round"
                fill="transparent"
                className="transition-all duration-1000 ease-out"
              />
            </svg>
            <div className="absolute flex flex-col items-center justify-center">
              <span className={`text-3xl font-extrabold ${scoreColor}`}>
                {result.risk_score}
              </span>
              <span className="text-[10px] uppercase tracking-wider text-muted-foreground">Risk Score</span>
            </div>
          </div>

          <div className="space-y-2 flex-1 text-center sm:text-left">
            <div className="flex flex-wrap items-center justify-center sm:justify-start gap-2.5">
              <RiskBadge level={result.risk_level} size="lg" />
              <span className="text-xs px-2.5 py-1 rounded-md bg-muted border border-border text-slate-300">
                Confidence: <strong className="capitalize text-white">{result.confidence}</strong>
              </span>
            </div>
            <p className="text-sm text-slate-300 leading-relaxed pt-1">
              {result.explanation}
            </p>
          </div>
        </div>

        {/* Recommendation Box */}
        <div className={`p-4 rounded-xl border ${
          result.risk_level === 'HIGH'
            ? 'bg-destructive/10 border-destructive/30 text-red-200'
            : result.risk_level === 'MEDIUM'
            ? 'bg-primary/10 border-primary/30 text-amber-200'
            : 'bg-success/10 border-success/30 text-emerald-200'
        }`}>
          <div className="flex items-start gap-3">
            {result.risk_level === 'HIGH' ? (
              <ShieldAlert className="w-5 h-5 text-destructive mt-0.5 flex-shrink-0" />
            ) : result.risk_level === 'MEDIUM' ? (
              <AlertCircle className="w-5 h-5 text-primary mt-0.5 flex-shrink-0" />
            ) : (
              <CheckCircle2 className="w-5 h-5 text-success mt-0.5 flex-shrink-0" />
            )}
            <div>
              <h4 className="text-sm font-semibold mb-1">Recommended Action</h4>
              <p className="text-xs sm:text-sm leading-relaxed opacity-90">{result.recommendation}</p>
            </div>
          </div>
        </div>

        {/* Detected Indicators List */}
        <div>
          <h4 className="text-sm font-semibold text-slate-300 mb-3 flex items-center gap-2">
            <span>Why This Was Flagged</span>
            <span className="text-xs px-2 py-0.5 rounded-full bg-primary/20 text-primary border border-primary/30">
              {result.indicators.length} Signals
            </span>
          </h4>

          {result.indicators.length === 0 ? (
            <p className="text-xs text-muted-foreground italic">No suspicious indicators triggered during static and heuristic scans.</p>
          ) : (
            <div className="space-y-2.5 max-h-60 overflow-y-auto pr-1">
              {result.indicators.map((ind, idx) => (
                <div
                  key={idx}
                  className="p-3.5 rounded-lg bg-secondary border border-border flex items-start gap-3 hover:border-border-light transition"
                >
                  <div className="mt-0.5">
                    {ind.severity === 'HIGH' ? (
                      <AlertOctagon className="w-4 h-4 text-destructive" />
                    ) : (
                      <AlertCircle className="w-4 h-4 text-primary" />
                    )}
                  </div>
                  <div className="flex-1">
                    <div className="flex items-center justify-between gap-2">
                      <span className="text-sm font-semibold text-white">{ind.title}</span>
                      <span className={`text-[10px] font-bold px-2 py-0.5 rounded uppercase tracking-wider ${
                        ind.severity === 'HIGH' ? 'bg-destructive/20 text-destructive' : 'bg-primary/20 text-primary'
                      }`}>
                        {ind.severity}
                      </span>
                    </div>
                    <p className="text-xs text-muted-foreground mt-1 leading-relaxed">{ind.description}</p>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>

        {/* Footer info note */}
        <div className="pt-2 border-t border-border flex items-center justify-between text-xs text-muted-foreground">
          <span>ScamShield AI • Explainable Pre-Transaction Assistant</span>
          <button
            onClick={onClose}
            className="px-5 py-2 bg-primary hover:bg-primary-hover text-primary-foreground font-bold rounded-lg text-xs transition"
          >
            Done
          </button>
        </div>
      </div>
    </div>
  );
};
