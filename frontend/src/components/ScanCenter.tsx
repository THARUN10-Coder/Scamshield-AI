import React, { useState } from 'react';
import { apiService } from '../services/api';
import { ScanResult } from '../types';
import {
  MessageSquare,
  Link2,
  QrCode,
  PhoneCall,
  CreditCard,
  Image as ImageIcon,
  Sparkles,
  Loader2,
  UploadCloud
} from 'lucide-react';

interface ScanCenterProps {
  onScanComplete: (result: ScanResult) => void;
}

export const ScanCenter: React.FC<ScanCenterProps> = ({ onScanComplete }) => {
  const [activeTab, setActiveTab] = useState<'message' | 'url' | 'qr' | 'phone' | 'payment' | 'screenshot'>('message');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // Form states
  const [messageText, setMessageText] = useState('');
  const [urlText, setUrlText] = useState('');
  const [phoneText, setPhoneText] = useState('');
  const [qrFile, setQrFile] = useState<File | null>(null);
  const [screenshotFile, setScreenshotFile] = useState<File | null>(null);

  // Payment form state
  const [paymentData, setPaymentData] = useState({
    recipient: '',
    amount: '',
    message: '',
    upi_id: '',
    phone: '',
    payment_method: 'UPI'
  });

  // Demo presets helper
  const loadDemoScenario = (scenario: string) => {
    setError(null);
    if (scenario === 'lottery') {
      setActiveTab('message');
      setMessageText('Congratulations! You have won ₹50,000 in Kaun Banega Crorepati lucky draw. Click http://kbc-reward-claim.top to claim money now and share OTP.');
    } else if (scenario === 'bank_kyc') {
      setActiveTab('message');
      setMessageText('URGENT! Your SBI account will be blocked today. Verify your KYC immediately by clicking http://sbi-kyc-update.xyz and submit your OTP.');
    } else if (scenario === 'electricity') {
      setActiveTab('message');
      setMessageText('Dear consumer, your BESCOM electricity power will be disconnected tonight at 9:30 PM due to unpaid bill of ₹1,450. Contact electricity officer immediately on 9876543210.');
    } else if (scenario === 'phishing_url') {
      setActiveTab('url');
      setUrlText('http://sbi-secure-login-update.xyz/verify-banking');
    } else if (scenario === 'safe_message') {
      setActiveTab('message');
      setMessageText('Your monthly electricity bill for meter 482910 is Rs 1,240. Due date is 28th Sep. Pay conveniently via your utility board portal or authorized app.');
    } else if (scenario === 'suspicious_payment') {
      setActiveTab('payment');
      setPaymentData({
        recipient: 'Unknown Merchant Support',
        amount: '8999',
        message: 'Pay immediately or legal warrant will be issued against your bank account.',
        upi_id: 'refund.desk.officer@okhdfcbank',
        phone: '+919876543210',
        payment_method: 'UPI'
      });
    }
  };

  const handleMessageScan = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!messageText.trim()) return;
    setLoading(true);
    setError(null);
    try {
      const res = await apiService.scanMessage(messageText);
      onScanComplete(res);
    } catch (err: any) {
      setError(err.message || 'Error analyzing message');
    } finally {
      setLoading(false);
    }
  };

  const handleUrlScan = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!urlText.trim()) return;
    setLoading(true);
    setError(null);
    try {
      const res = await apiService.scanUrl(urlText);
      onScanComplete(res);
    } catch (err: any) {
      setError(err.message || 'Error analyzing URL');
    } finally {
      setLoading(false);
    }
  };

  const handleQrScan = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!qrFile) return;
    setLoading(true);
    setError(null);
    try {
      const res = await apiService.scanQr(qrFile);
      onScanComplete(res);
    } catch (err: any) {
      setError(err.message || 'We couldn\'t decode this QR image. Try uploading a clearer image.');
    } finally {
      setLoading(false);
    }
  };

  const handlePhoneScan = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!phoneText.trim()) return;
    setLoading(true);
    setError(null);
    try {
      const res = await apiService.scanPhone(phoneText);
      onScanComplete(res);
    } catch (err: any) {
      setError(err.message || 'Error analyzing phone number');
    } finally {
      setLoading(false);
    }
  };

  const handlePaymentScan = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!paymentData.recipient.trim()) return;
    setLoading(true);
    setError(null);
    try {
      const res = await apiService.scanPayment({
        recipient: paymentData.recipient,
        amount: paymentData.amount ? parseFloat(paymentData.amount) : undefined,
        message: paymentData.message,
        upi_id: paymentData.upi_id,
        phone: paymentData.phone,
        payment_method: paymentData.payment_method
      });
      onScanComplete(res);
    } catch (err: any) {
      setError(err.message || 'Error analyzing payment details');
    } finally {
      setLoading(false);
    }
  };

  const handleScreenshotScan = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!screenshotFile) return;
    setLoading(true);
    setError(null);
    try {
      const res = await apiService.scanScreenshot(screenshotFile);
      onScanComplete(res);
    } catch (err: any) {
      setError(err.message || 'Failed to analyze screenshot');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-6">
      {/* Demo Scenario Shortcuts Bar */}
      <div className="p-4 rounded-xl glass-card flex flex-wrap items-center justify-between gap-3 border-l-4 border-l-primary bg-card">
        <div className="flex items-center gap-2">
          <Sparkles className="w-4 h-4 text-primary" />
          <span className="text-xs font-semibold text-slate-300">Demonstration Presets:</span>
        </div>
        <div className="flex flex-wrap gap-2">
          <button
            onClick={() => loadDemoScenario('bank_kyc')}
            className="px-3 py-1.5 text-xs rounded-md bg-secondary hover:bg-muted text-slate-200 border border-border transition font-medium"
          >
            Bank KYC Scam
          </button>
          <button
            onClick={() => loadDemoScenario('electricity')}
            className="px-3 py-1.5 text-xs rounded-md bg-secondary hover:bg-muted text-slate-200 border border-border transition font-medium"
          >
            Electricity Bill Cutoff
          </button>
          <button
            onClick={() => loadDemoScenario('lottery')}
            className="px-3 py-1.5 text-xs rounded-md bg-secondary hover:bg-muted text-slate-200 border border-border transition font-medium"
          >
            Lottery Bait
          </button>
          <button
            onClick={() => loadDemoScenario('phishing_url')}
            className="px-3 py-1.5 text-xs rounded-md bg-secondary hover:bg-muted text-slate-200 border border-border transition font-medium"
          >
            Spoofed Bank URL
          </button>
          <button
            onClick={() => loadDemoScenario('suspicious_payment')}
            className="px-3 py-1.5 text-xs rounded-md bg-secondary hover:bg-muted text-slate-200 border border-border transition font-medium"
          >
            Extortion Payment
          </button>
          <button
            onClick={() => loadDemoScenario('safe_message')}
            className="px-3 py-1.5 text-xs rounded-md bg-success/15 text-success hover:bg-success/25 border border-success/30 transition font-medium"
          >
            Safe Transaction
          </button>
        </div>
      </div>

      {/* Main Scanner Container */}
      <div className="glass-panel rounded-2xl p-6 md:p-8 space-y-6 bg-card border border-border">
        {/* Navigation Tabs (shadcn style) */}
        <div className="flex flex-wrap gap-2 border-b border-border pb-4">
          {[
            { id: 'message', label: 'Message / SMS', icon: MessageSquare },
            { id: 'url', label: 'Website Link', icon: Link2 },
            { id: 'qr', label: 'QR Code', icon: QrCode },
            { id: 'phone', label: 'Phone Number', icon: PhoneCall },
            { id: 'payment', label: 'Payment Request', icon: CreditCard },
            { id: 'screenshot', label: 'Screenshot', icon: ImageIcon },
          ].map((tab) => {
            const Icon = tab.icon;
            const active = activeTab === tab.id;
            return (
              <button
                key={tab.id}
                onClick={() => {
                  setActiveTab(tab.id as any);
                  setError(null);
                }}
                className={`flex items-center gap-2 px-4 py-2.5 rounded-lg font-medium text-xs sm:text-sm transition-all ${
                  active
                    ? 'bg-primary text-primary-foreground font-bold shadow-md shadow-primary/10'
                    : 'text-muted-foreground hover:text-white hover:bg-secondary'
                }`}
              >
                <Icon className="w-4 h-4" />
                <span>{tab.label}</span>
              </button>
            );
          })}
        </div>

        {/* Error notification */}
        {error && (
          <div className="p-4 rounded-xl bg-destructive/10 border border-destructive/30 text-destructive text-xs sm:text-sm flex items-center justify-between">
            <span>{error}</span>
            <button onClick={() => setError(null)} className="text-destructive hover:opacity-80 font-bold">✕</button>
          </div>
        )}

        {/* Tab Content Panels */}
        {activeTab === 'message' && (
          <form onSubmit={handleMessageScan} className="space-y-4">
            <div>
              <label className="block text-xs font-semibold uppercase tracking-wider text-muted-foreground mb-2">
                Paste suspicious SMS, WhatsApp message, or email text
              </label>
              <textarea
                rows={4}
                value={messageText}
                onChange={(e) => setMessageText(e.target.value)}
                placeholder="Example: Congratulations! You have won ₹50,000. Click this link immediately to claim your reward..."
                className="w-full rounded-xl bg-secondary border border-border p-4 text-sm text-white placeholder:text-muted-foreground focus:outline-none focus:border-primary transition"
              />
            </div>
            <div className="flex items-center justify-between pt-2">
              <span className="text-xs text-muted-foreground">
                Extracts: Urgency language, threats, OTP solicitations, prize lures, impersonation.
              </span>
              <button
                type="submit"
                disabled={loading || !messageText.trim()}
                className="flex items-center gap-2 px-6 py-2.5 rounded-lg bg-primary hover:bg-primary-hover text-primary-foreground font-bold text-sm transition disabled:opacity-50"
              >
                {loading ? <Loader2 className="w-4 h-4 animate-spin" /> : <Sparkles className="w-4 h-4" />}
                <span>Analyze Message</span>
              </button>
            </div>
          </form>
        )}

        {activeTab === 'url' && (
          <form onSubmit={handleUrlScan} className="space-y-4">
            <div>
              <label className="block text-xs font-semibold uppercase tracking-wider text-muted-foreground mb-2">
                Enter Website or Payment Link (Static safe analysis without remote loading)
              </label>
              <input
                type="text"
                value={urlText}
                onChange={(e) => setUrlText(e.target.value)}
                placeholder="https://sbi-login-verify-kyc.xyz or http://192.168.1.1/pay"
                className="w-full rounded-xl bg-secondary border border-border p-4 text-sm text-white placeholder:text-muted-foreground focus:outline-none focus:border-primary transition"
              />
            </div>
            <div className="flex items-center justify-between pt-2">
              <span className="text-xs text-muted-foreground">
                Evaluates: IP hosts, suspicious TLDs, typosquatting, shorteners, credential keywords.
              </span>
              <button
                type="submit"
                disabled={loading || !urlText.trim()}
                className="flex items-center gap-2 px-6 py-2.5 rounded-lg bg-primary hover:bg-primary-hover text-primary-foreground font-bold text-sm transition disabled:opacity-50"
              >
                {loading ? <Loader2 className="w-4 h-4 animate-spin" /> : <Link2 className="w-4 h-4" />}
                <span>Scan URL</span>
              </button>
            </div>
          </form>
        )}

        {activeTab === 'qr' && (
          <form onSubmit={handleQrScan} className="space-y-4">
            <div className="border-2 border-dashed border-border rounded-2xl p-8 text-center bg-secondary/50 hover:bg-secondary transition cursor-pointer relative">
              <input
                type="file"
                accept="image/*"
                onChange={(e) => setQrFile(e.target.files?.[0] || null)}
                className="absolute inset-0 opacity-0 cursor-pointer w-full h-full"
              />
              <div className="flex flex-col items-center justify-center space-y-3">
                <div className="p-3 rounded-full bg-primary/10 text-primary">
                  <QrCode className="w-8 h-8" />
                </div>
                <div>
                  <p className="text-sm font-semibold text-white">
                    {qrFile ? qrFile.name : 'Upload QR Code Image'}
                  </p>
                  <p className="text-xs text-muted-foreground mt-1">
                    Supports PNG, JPG, WebP containing UPI payment codes or links.
                  </p>
                </div>
              </div>
            </div>
            <div className="flex items-center justify-between pt-2">
              <span className="text-xs text-muted-foreground">
                Decodes payee VPA, merchant parameters, and verifies whether money will leave your account.
              </span>
              <button
                type="submit"
                disabled={loading || !qrFile}
                className="flex items-center gap-2 px-6 py-2.5 rounded-lg bg-primary hover:bg-primary-hover text-primary-foreground font-bold text-sm transition disabled:opacity-50"
              >
                {loading ? <Loader2 className="w-4 h-4 animate-spin" /> : <UploadCloud className="w-4 h-4" />}
                <span>Decode & Analyze QR</span>
              </button>
            </div>
          </form>
        )}

        {activeTab === 'phone' && (
          <form onSubmit={handlePhoneScan} className="space-y-4">
            <div>
              <label className="block text-xs font-semibold uppercase tracking-wider text-muted-foreground mb-2">
                Phone Number or Customer Care Helpline
              </label>
              <input
                type="text"
                value={phoneText}
                onChange={(e) => setPhoneText(e.target.value)}
                placeholder="+919876543210 or +923001234567 or 1800-XXX-XXXX"
                className="w-full rounded-xl bg-secondary border border-border p-4 text-sm text-white placeholder:text-muted-foreground focus:outline-none focus:border-primary transition"
              />
            </div>
            <div className="flex items-center justify-between pt-2">
              <span className="text-xs text-muted-foreground">
                Detects: High-risk foreign dial codes, personal mobiles posing as corporate helplines.
              </span>
              <button
                type="submit"
                disabled={loading || !phoneText.trim()}
                className="flex items-center gap-2 px-6 py-2.5 rounded-lg bg-primary hover:bg-primary-hover text-primary-foreground font-bold text-sm transition disabled:opacity-50"
              >
                {loading ? <Loader2 className="w-4 h-4 animate-spin" /> : <PhoneCall className="w-4 h-4" />}
                <span>Analyze Number</span>
              </button>
            </div>
          </form>
        )}

        {activeTab === 'payment' && (
          <form onSubmit={handlePaymentScan} className="space-y-4">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label className="block text-xs font-semibold uppercase tracking-wider text-muted-foreground mb-2">
                  Recipient Name / Organization *
                </label>
                <input
                  type="text"
                  required
                  value={paymentData.recipient}
                  onChange={(e) => setPaymentData({ ...paymentData, recipient: e.target.value })}
                  placeholder="e.g. Unknown Merchant, BESCOM Officer, HDFC Support"
                  className="w-full rounded-xl bg-secondary border border-border p-3 text-sm text-white placeholder:text-muted-foreground focus:outline-none focus:border-primary transition"
                />
              </div>

              <div>
                <label className="block text-xs font-semibold uppercase tracking-wider text-muted-foreground mb-2">
                  Requested Amount (₹)
                </label>
                <input
                  type="number"
                  step="any"
                  value={paymentData.amount}
                  onChange={(e) => setPaymentData({ ...paymentData, amount: e.target.value })}
                  placeholder="e.g. 8999"
                  className="w-full rounded-xl bg-secondary border border-border p-3 text-sm text-white placeholder:text-muted-foreground focus:outline-none focus:border-primary transition"
                />
              </div>

              <div>
                <label className="block text-xs font-semibold uppercase tracking-wider text-muted-foreground mb-2">
                  Payee UPI ID (VPA)
                </label>
                <input
                  type="text"
                  value={paymentData.upi_id}
                  onChange={(e) => setPaymentData({ ...paymentData, upi_id: e.target.value })}
                  placeholder="e.g. refund.desk@okhdfcbank"
                  className="w-full rounded-xl bg-secondary border border-border p-3 text-sm text-white placeholder:text-muted-foreground focus:outline-none focus:border-primary transition"
                />
              </div>

              <div>
                <label className="block text-xs font-semibold uppercase tracking-wider text-muted-foreground mb-2">
                  Payment Method
                </label>
                <select
                  value={paymentData.payment_method}
                  onChange={(e) => setPaymentData({ ...paymentData, payment_method: e.target.value })}
                  className="w-full rounded-xl bg-secondary border border-border p-3 text-sm text-white focus:outline-none focus:border-primary transition"
                >
                  <option value="UPI">UPI (Google Pay, PhonePe, Paytm)</option>
                  <option value="NetBanking">NetBanking / IMPS</option>
                  <option value="Card">Debit / Credit Card</option>
                  <option value="QR">Static Merchant QR</option>
                </select>
              </div>
            </div>

            <div>
              <label className="block text-xs font-semibold uppercase tracking-wider text-muted-foreground mb-2">
                Contextual Message or Stated Reason
              </label>
              <textarea
                rows={2}
                value={paymentData.message}
                onChange={(e) => setPaymentData({ ...paymentData, message: e.target.value })}
                placeholder="e.g. Pay immediately or your power supply will be terminated tonight."
                className="w-full rounded-xl bg-secondary border border-border p-3 text-sm text-white placeholder:text-muted-foreground focus:outline-none focus:border-primary transition"
              />
            </div>

            <div className="flex items-center justify-between pt-2">
              <span className="text-xs text-muted-foreground">
                Cross-evaluates recipient legitimacy, penny-drop test amounts, and urgency cues.
              </span>
              <button
                type="submit"
                disabled={loading || !paymentData.recipient.trim()}
                className="flex items-center gap-2 px-6 py-2.5 rounded-lg bg-primary hover:bg-primary-hover text-primary-foreground font-bold text-sm transition disabled:opacity-50"
              >
                {loading ? <Loader2 className="w-4 h-4 animate-spin" /> : <CreditCard className="w-4 h-4" />}
                <span>Evaluate Payment Request</span>
              </button>
            </div>
          </form>
        )}

        {activeTab === 'screenshot' && (
          <form onSubmit={handleScreenshotScan} className="space-y-4">
            <div className="border-2 border-dashed border-border rounded-2xl p-8 text-center bg-secondary/50 hover:bg-secondary transition cursor-pointer relative">
              <input
                type="file"
                accept="image/*"
                onChange={(e) => setScreenshotFile(e.target.files?.[0] || null)}
                className="absolute inset-0 opacity-0 cursor-pointer w-full h-full"
              />
              <div className="flex flex-col items-center justify-center space-y-3">
                <div className="p-3 rounded-full bg-primary/10 text-primary">
                  <ImageIcon className="w-8 h-8" />
                </div>
                <div>
                  <p className="text-sm font-semibold text-white">
                    {screenshotFile ? screenshotFile.name : 'Upload Screenshot of Chat, SMS, or Payment Prompt'}
                  </p>
                  <p className="text-xs text-muted-foreground mt-1">
                    Extracts embedded text, links, and UPI IDs for end-to-end multi-signal evaluation.
                  </p>
                </div>
              </div>
            </div>
            <div className="flex items-center justify-between pt-2">
              <span className="text-xs text-muted-foreground">
                Local OCR pipeline with heuristic fallback extraction.
              </span>
              <button
                type="submit"
                disabled={loading || !screenshotFile}
                className="flex items-center gap-2 px-6 py-2.5 rounded-lg bg-primary hover:bg-primary-hover text-primary-foreground font-bold text-sm transition disabled:opacity-50"
              >
                {loading ? <Loader2 className="w-4 h-4 animate-spin" /> : <UploadCloud className="w-4 h-4" />}
                <span>Analyze Screenshot</span>
              </button>
            </div>
          </form>
        )}
      </div>
    </div>
  );
};
