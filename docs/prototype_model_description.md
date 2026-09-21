# ScamShield AI — Prototype Model Description

> **System Designation**: ScamShield AI (MVP Prototype v1.0)  
> **Classification**: Defensive Cybersecurity & Explainable AI (XAI) Pre-Transaction Fraud Prevention System  
> **Target Environment**: College / Hackathon Demonstration & Academic Proof of Concept (PoC)

---

## 1. Project Abstract & Prototype Scope
**ScamShield AI** is an explainable, multi-signal AI prototype designed to shift digital payment fraud defense from a reactive post-incident model to a **pre-transaction interception model**. 

Traditional banking security systems trigger alerts only after an unauthorized transfer has taken place or a card has been compromised. In contrast, this prototype analyzes untrusted inputs (suspicious SMS alerts, phishing links, UPI QR codes, fraudulent customer-care numbers, and coercive payment requests) **before** the user authorizes payment or discloses sensitive banking credentials.

---

## 2. Architectural Prototype Pipeline

```
+-----------------------------------------------------------------------------------+
|                            INGESTION LAYER (SCAN CENTER)                          |
|  • SMS / Message Text   • Website Link / URL   • UPI QR Image   • Phone / Helpline|
|  • Structured Payment Parameters (VPA, Payee Name, Note)  • Screenshot / Chat Log |
+-----------------------------------------------------------------------------------+
                                          │
                                          ▼
+-----------------------------------------------------------------------------------+
|                     FEATURE EXTRACTION & DETECTION ENGINES                        |
|                                                                                   |
|  [NLP Rule Detector]       [ML Classifier Engine]     [Static URL Inspector]     |
|  • Urgency keywords        • TF-IDF Vectorizer        • IP-based hostnames        |
|  • Account block threats   • Logistic Regression      • Phishing TLDs (.xyz, etc.)|
|  • Credential solicitation • Probability estimation   • Brand typosquatting       |
|  • Brand impersonation                                • URL shorteners            |
|                                                                                   |
|  [QR & UPI Parser]         [Telephony Analyzer]       [Payment Context Analyzer]  |
|  • `upi://pay` decoder     • Toll-free verification   • Coercive notes            |
|  • Payee VPA validation    • Domestic vs Foreign codes• High value / penny-drop   |
+-----------------------------------------------------------------------------------+
                                          │
                                          ▼
+-----------------------------------------------------------------------------------+
|                        MULTI-SIGNAL RISK FUSION ENGINE                            |
|                                                                                   |
|  • Weighted Signal Aggregation:                                                   |
|    Score = w1*(NLP/ML) + w2*(URL) + w3*(Phone) + w4*(Payment Context)             |
|  • Multi-Vector Synergy Escalation (e.g. Threatening SMS + Phishing URL = Flag)   |
|  • Calibrated Risk Normalization: 0 to 100 Scale                                  |
|  • Threshold Partitioning: LOW (0-29), MEDIUM (30-69), HIGH (70-100)              |
+-----------------------------------------------------------------------------------+
                                          │
                                          ▼
+-----------------------------------------------------------------------------------+
|                         EXPLAINABLE AI (XAI) OUTPUT LAYER                         |
|                                                                                   |
|  • Numerical Risk Score (e.g., 85/100)                                            |
|  • Categorical Risk Level Badge (LOW / MEDIUM / HIGH)                             |
|  • Itemized Signal Indicators (Exact reason triggers, e.g., "Urgency", "Threat")  |
|  • Contextual Natural-Language Explanation                                        |
|  • Actionable Defensive Recommendation ("Never enter UPI PIN to receive money")   |
|  • Calibrated Confidence Indicator (Low / Medium / High)                          |
+-----------------------------------------------------------------------------------+
```

---

## 3. Prototype Modules & Technological Stack

| Subsystem | Components | Purpose in Prototype |
| :--- | :--- | :--- |
| **User Interface** | React 18, Vite, TypeScript, Tailwind CSS, Recharts, Lucide Icons | High-contrast **baroworks dark theme** interface with circular risk meters, analytics charts, and 6 one-click demo presets. |
| **API Backend** | FastAPI, Python 3.13, Pydantic v2, Uvicorn | High-throughput asynchronous endpoints with automated OpenAPI (Swagger) schema validation. |
| **AI / ML Engine** | scikit-learn, TF-IDF Vectorizer, Logistic Regression, NumPy | Lightweight, explainable binary classification trained on real-world scam heuristics and conversational patterns. |
| **Computer Vision**| Pillow (PIL), OpenCV / Pyzbar QR Decoder | Decodes static QR codes and extracts UPI query parameters (`pa`, `pn`, `am`, `tn`) without network calls. |
| **Database & Audit**| SQLite (PostgreSQL compatible), SQLAlchemy ORM | Stores anonymized audit records using SHA-256 hashed inputs to preserve privacy. |

---

## 4. Key Innovations of the Prototype
1. **Explainable AI over Black-Box Scoring**: Every risk score is accompanied by granular, auditable indicators (e.g. *Account Block Threat*, *Impersonation VPA*, *High-Risk TLD*).
2. **Defensive Zero-Trust Principles**:
   - Never accesses dangerous remote URLs during scanning (purely static evaluation).
   - Never requests, captures, or persists UPI PINs, ATM PINs, banking passwords, or OTPs.
3. **Cross-Signal Synergy Fusion**: Evaluates combinations of disparate vectors (e.g. a benign-looking message combined with a spoofed payment handle) that single-vector antivirus tools fail to flag.

---

## 5. Prototype Presentation Points (For Hackathons & Project Reviews)
- **Central Thesis**: *"ScamShield AI is an explainable, pre-transaction, multi-signal fraud-risk assistant."*
- **Tone & Calibrated Language**: Formulated as a **Risk Assessment** and **Suspicious Indicator Detector**, not an absolute or infallible guarantee.
- **Demonstration Ready**: Equipped with 6 built-in presets (Bank KYC Scam, BESCOM Electricity Threat, KBC Lottery Bait, Spoofed Bank Link, Extortion Transfer, and Safe Transaction).
