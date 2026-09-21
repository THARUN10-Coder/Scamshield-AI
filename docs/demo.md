# ScamShield AI Demo & Hackathon Presentation Script

## 5-Minute Pitch Sequence

### Minute 1: The Core Problem & Philosophy
- **Presenter**: "Every year, millions of victims lose money to digital payment scams—not because the bank's encryption failed, but because social engineering deceived the victim into authorizing the transaction themselves."
- **The Paradigm Shift**:
  - *Traditional Bank Defense*: Transaction occurs $\rightarrow$ Fraud detected hours/days later $\rightarrow$ Damage already done.
  - *ScamShield AI*: Suspicious interaction received $\rightarrow$ Explainable pre-transaction AI risk evaluation $\rightarrow$ Warning $\rightarrow$ User halts payment.

### Minute 2: Demo Scenario 1 — Fake Electricity Cutoff SMS
1. Open the ScamShield AI application.
2. Click **Scan Center** or use the preset button **"Electricity Bill Cutoff"**.
3. Point out the input:
   > *"Dear consumer, your BESCOM electricity power will be disconnected tonight at 9:30 PM due to unpaid bill of ₹1,450. Contact electricity officer immediately on 9876543210."*
4. Click **Analyze Message**.
5. Show the **Result Modal**:
   - **Risk Level**: HIGH RISK (Score ~80–90/100).
   - **Explainability**: Point to the exact detected indicators:
     - *Urgency*: "tonight at 9:30 PM"
     - *Threat*: "power will be disconnected"
     - *Impersonation*: "BESCOM electricity officer"
     - *Personal Mobile Line*: 10-digit number used instead of official 1800 helpline.
   - **Recommendation**: Instructs user to verify through official Bescom portal.

### Minute 3: Demo Scenario 2 — Spoofed Bank Phishing URL
1. Switch to **Website Link** tab or select **"Spoofed Bank URL"**.
2. URL: `http://sbi-secure-login-update.xyz/verify-banking`
3. Click **Scan URL**.
4. Highlight explainable indicators:
   - High-risk TLD (`.xyz`)
   - Unencrypted HTTP protocol
   - Brand keyword spoofing (`sbi`) outside official domain.
   - Credential bait keywords (`login`, `update`, `verify`).

### Minute 4: Demo Scenario 3 — Extortion Payment Request & QR Evaluation
1. Switch to **Payment Request** tab or select **"Extortion Payment"**.
2. Highlight how recipient name ("Unknown Merchant Support") combined with coercive notes triggers high-risk classification.
3. Show the **QR Code Scanner** and demonstrate how UPI URIs are decoded safely without transferring funds.

### Minute 5: Dashboard Analytics & Conclusion
1. Navigate to **Dashboard**.
2. Point to the live Recharts visualizations:
   - Risk distribution (Low vs. Medium vs. High).
   - Scans grouped by vector (SMS, URL, Phone, QR).
3. Conclude:
   > *"ScamShield AI is an explainable, multi-signal, pre-transaction fraud defense assistant. It empowers users with clarity before they pay."*
