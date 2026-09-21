import React from 'react';
import {
  ShieldAlert,
  KeyRound,
  QrCode,
  PhoneCall,
  Lock,
  AlertTriangle,
  FileCheck
} from 'lucide-react';

export const SafetyCenterView: React.FC = () => {
  const safetyRules = [
    {
      title: 'UPI PIN is ONLY for Sending Money',
      subtitle: 'Never enter your PIN to receive payments or refunds',
      icon: KeyRound,
      color: 'text-primary',
      bgColor: 'bg-primary/15',
      description:
        'A common social engineering trick is sending a collect request or QR code claiming it will "deposit a cashback into your account." In UPI architecture, receiving money never requires entering your UPI PIN or biometric authentication.',
    },
    {
      title: 'QR Code Traps & Pre-filled Amounts',
      subtitle: 'Inspect what you scan before hitting confirm',
      icon: QrCode,
      color: 'text-primary',
      bgColor: 'bg-primary/15',
      description:
        'Scammers send QR codes via WhatsApp for OLX sale purchases or refund settlements. Scanning a QR code always authorizes an OUTBOUND transfer from your bank account to the recipient.',
    },
    {
      title: 'Fake Electricity & Utility Cutoff Alerts',
      subtitle: 'Verify power disconnection alerts exclusively via official apps',
      icon: AlertTriangle,
      color: 'text-destructive',
      bgColor: 'bg-destructive/15',
      description:
        'Electricity boards (BESCOM, TNEB, UPPCL, etc.) never send SMS from personal 10-digit mobile numbers threatening immediate disconnection at 9:30 PM. Always check your consumer number directly on official utility apps.',
    },
    {
      title: 'Customer Care Number Search Spoofing',
      subtitle: 'Do not trust top Google Search results for customer support',
      icon: PhoneCall,
      color: 'text-primary',
      bgColor: 'bg-primary/15',
      description:
        'Fraudsters register business profiles on search engines with their personal numbers pretending to be Swiggy, Zomato, SBI, or PhonePe customer care. Always fetch helpline numbers from the official app settings.',
    },
    {
      title: 'Screen-Sharing App Scams (AnyDesk, RustDesk)',
      subtitle: 'Never install remote access software on caller instructions',
      icon: Lock,
      color: 'text-success',
      bgColor: 'bg-success/15',
      description:
        'Imposters ask victims to install screen-sharing software under the pretext of "helping verify KYC" or "reversing a failed transaction". Once installed, they capture your OTPs and banking credentials in real time.',
    },
    {
      title: 'Part-Time Telegram Job & Task Scams',
      subtitle: 'Beware of "Rate hotels or like YouTube videos to earn ₹5,000/day"',
      icon: FileCheck,
      color: 'text-primary',
      bgColor: 'bg-primary/15',
      description:
        'Victims receive initial small payouts (₹150–₹300) to build false trust, after which they are pressured into "prepaid merchant tasks" or crypto deposits amounting to lakhs before withdrawals are frozen.',
    },
  ];

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="glass-panel bg-card border border-border p-6 md:p-8 rounded-2xl space-y-2">
        <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-primary/15 text-primary border border-primary/30 text-xs font-semibold">
          <ShieldAlert className="w-4 h-4" />
          Pre-Transaction Education
        </div>
        <h2 className="text-2xl font-bold text-white tracking-tight">Cybersecurity & UPI Safety Center</h2>
        <p className="text-sm text-muted-foreground max-w-2xl leading-relaxed">
          Defensive security principles to safeguard your digital banking credentials, UPI VPAs, and personal identities.
        </p>
      </div>

      {/* Safety Cards Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {safetyRules.map((rule, idx) => {
          const Icon = rule.icon;
          return (
            <div
              key={idx}
              className="glass-card bg-card p-6 rounded-2xl border border-border space-y-4 hover:border-border-light transition flex flex-col justify-between"
            >
              <div className="space-y-3">
                <div className={`w-12 h-12 rounded-xl ${rule.bgColor} flex items-center justify-center`}>
                  <Icon className={`w-6 h-6 ${rule.color}`} />
                </div>
                <h3 className="text-base font-bold text-white tracking-tight">{rule.title}</h3>
                <p className="text-xs font-semibold text-primary">{rule.subtitle}</p>
                <p className="text-xs text-slate-300 leading-relaxed">{rule.description}</p>
              </div>

              <div className="pt-3 border-t border-border text-[11px] text-muted-foreground flex items-center gap-1.5">
                <Lock className="w-3.5 h-3.5 text-primary" />
                <span>Zero-Trust Defensive Guideline</span>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
};
