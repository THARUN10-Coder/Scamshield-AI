import React, { useState } from 'react';
import { apiService } from '../services/api';
import { Flag, Send, CheckCircle, AlertOctagon, Loader2 } from 'lucide-react';

export const ReportView: React.FC = () => {
  const [scamType, setScamType] = useState('UPI Fraud');
  const [description, setDescription] = useState('');
  const [evidenceUrl, setEvidenceUrl] = useState('');
  const [evidencePhone, setEvidencePhone] = useState('');
  const [submitting, setSubmitting] = useState(false);
  const [submitted, setSubmitted] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!description.trim()) return;
    setSubmitting(true);
    try {
      await apiService.submitReport({
        scam_type: scamType,
        description,
        evidence_url: evidenceUrl.trim() || undefined,
        evidence_phone: evidencePhone.trim() || undefined,
      });
      setSubmitted(true);
    } catch (err) {
      alert('Failed to submit report. Please try again.');
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className="max-w-2xl mx-auto space-y-6">
      <div className="glass-panel bg-card border border-border p-6 md:p-8 rounded-2xl space-y-6">
        <div className="flex items-center gap-3 border-b border-border pb-4">
          <div className="p-2.5 rounded-xl bg-destructive/15 text-destructive">
            <Flag className="w-5 h-5" />
          </div>
          <div>
            <h2 className="text-xl font-bold text-white tracking-tight">Report Emerging Scam Pattern</h2>
            <p className="text-xs text-muted-foreground">
              Community telemetry helps refine ScamShield AI's defensive detection heuristics
            </p>
          </div>
        </div>

        {submitted ? (
          <div className="p-8 text-center space-y-4 rounded-xl bg-secondary border border-success/30">
            <div className="w-12 h-12 rounded-full bg-success/15 text-success flex items-center justify-center mx-auto">
              <CheckCircle className="w-6 h-6" />
            </div>
            <h3 className="text-lg font-bold text-white">Thank you for reporting!</h3>
            <p className="text-sm text-slate-300 max-w-md mx-auto leading-relaxed">
              Your anonymous report helps improve future scam detection and protects fellow citizens from digital fraud.
            </p>
            <button
              onClick={() => {
                setSubmitted(false);
                setDescription('');
                setEvidenceUrl('');
                setEvidencePhone('');
              }}
              className="px-5 py-2.5 rounded-lg bg-primary text-primary-foreground font-bold text-xs hover:bg-primary-hover transition"
            >
              Submit Another Report
            </button>
          </div>
        ) : (
          <form onSubmit={handleSubmit} className="space-y-4">
            <div>
              <label className="block text-xs font-semibold uppercase tracking-wider text-muted-foreground mb-2">
                Scam Category *
              </label>
              <select
                value={scamType}
                onChange={(e) => setScamType(e.target.value)}
                className="w-full rounded-xl bg-secondary border border-border p-3 text-sm text-white focus:outline-none focus:border-primary transition"
              >
                <option value="UPI Fraud">UPI Collect Request / Fraud</option>
                <option value="Phishing Link">Phishing SMS / Website</option>
                <option value="Electricity Threat">Electricity / Utility Cutoff Scam</option>
                <option value="Bank KYC Expiry">Fake Bank KYC Expiry</option>
                <option value="Job / Telegram Scam">Telegram Part-time Job Bait</option>
                <option value="Customer Care Spoof">Fake Customer Care Number</option>
                <option value="Lottery / Prize">Lottery / Cash Prize Bait</option>
              </select>
            </div>

            <div>
              <label className="block text-xs font-semibold uppercase tracking-wider text-muted-foreground mb-2">
                Detailed Description of Scam Incident *
              </label>
              <textarea
                required
                rows={4}
                value={description}
                onChange={(e) => setDescription(e.target.value)}
                placeholder="Explain the sequence of events, message sent to you, or payment requested..."
                className="w-full rounded-xl bg-secondary border border-border p-4 text-sm text-white placeholder:text-muted-foreground focus:outline-none focus:border-primary transition"
              />
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label className="block text-xs font-semibold uppercase tracking-wider text-muted-foreground mb-2">
                  Suspicious Website URL (Optional)
                </label>
                <input
                  type="text"
                  value={evidenceUrl}
                  onChange={(e) => setEvidenceUrl(e.target.value)}
                  placeholder="https://malicious-site.xyz"
                  className="w-full rounded-xl bg-secondary border border-border p-3 text-sm text-white placeholder:text-muted-foreground focus:outline-none focus:border-primary transition"
                />
              </div>

              <div>
                <label className="block text-xs font-semibold uppercase tracking-wider text-muted-foreground mb-2">
                  Suspicious Contact Phone (Optional)
                </label>
                <input
                  type="text"
                  value={evidencePhone}
                  onChange={(e) => setEvidencePhone(e.target.value)}
                  placeholder="+9198XXXXXXXX"
                  className="w-full rounded-xl bg-secondary border border-border p-3 text-sm text-white placeholder:text-muted-foreground focus:outline-none focus:border-primary transition"
                />
              </div>
            </div>

            <div className="p-3 rounded-xl bg-secondary border border-border flex items-center gap-3 text-xs text-muted-foreground">
              <AlertOctagon className="w-4 h-4 text-primary flex-shrink-0" />
              <span>Privacy notice: Do not submit your own passwords, OTPs, or bank card CVVs.</span>
            </div>

            <button
              type="submit"
              disabled={submitting || !description.trim()}
              className="w-full flex items-center justify-center gap-2 py-3 rounded-lg bg-primary hover:bg-primary-hover text-primary-foreground font-bold text-sm transition disabled:opacity-50"
            >
              {submitting ? <Loader2 className="w-4 h-4 animate-spin" /> : <Send className="w-4 h-4" />}
              <span>Submit Scam Telemetry</span>
            </button>
          </form>
        )}
      </div>
    </div>
  );
};
