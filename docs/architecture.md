# ScamShield AI Architecture Documentation

## 1. System Overview
ScamShield AI is an explainable, pre-transaction digital payment fraud prevention system. Rather than detecting fraud after financial settlement or unauthorized debit has already taken place, ScamShield evaluates untrusted inputs BEFORE authorization occurs.

```
                  +---------------------------------------------------+
                  |                 USER / VICTIM                     |
                  +---------------------------------------------------+
                                            |
                         (Submits suspicious input)
                                            v
     +-------------------------------------------------------------------------+
     |                       SCAMSHIELD AI SCAN CENTER                         |
     |  [SMS / Text]   [URL Link]   [UPI QR Code]   [Phone]   [Payment Form]   |
     +-------------------------------------------------------------------------+
                                            |
                                            v
     +-------------------------------------------------------------------------+
     |                    MULTI-SIGNAL AI RISK ENGINE                          |
     |                                                                         |
     |  1. NLP Feature Extractor (Urgency, Threats, Impersonation, Credential) |
     |  2. ML Classifier (TF-IDF + Logistic Regression statistical scoring)   |
     |  3. Safe Static URL Inspector (IP host, Typosquatting, High-risk TLDs)  |
     |  4. Safe QR Code Payload Decoder (UPI URI structure & VPA semantics)    |
     |  5. Dialing & Customer-Care Heuristics (Spoofing & Foreign Call Codes)  |
     |  6. Multi-Signal Fusion Engine (Weighted cross-signal aggregation)      |
     +-------------------------------------------------------------------------+
                                            |
                                            v
     +-------------------------------------------------------------------------+
     |                       EXPLAINABLE OUTPUT LAYER                          |
     |                                                                         |
     |  • Risk Score (0 - 100)                                                 |
     |  • Risk Level (LOW / MEDIUM / HIGH)                                     |
     |  • Detected Signal Indicators (Exact reason tags and context)           |
     |  • Plain-Language Justification & Actionable Recommendations            |
     |  • Confidence Level (Low / Medium / High)                               |
     +-------------------------------------------------------------------------+
                                            |
                                            v
     +-------------------------------------------------------------------------+
     |                    AUDIT & COMMUNITY TELEMETRY                          |
     |                                                                         |
     |  • SQLite / PostgreSQL Storage (Hashed inputs, zero plain credentials)  |
     |  • Aggregated Anonymous Analytics & Trend Visualizations                |
     +-------------------------------------------------------------------------+
```

## 2. Defensive Security Design Principles
1. **Zero-Trust Input Sanitization**:
   - URLs submitted for analysis are NEVER fetched or loaded into an active browser context on the server. All inspection is strictly static and structural.
2. **Credential Redaction**:
   - No payment PINs, passwords, or OTPs are requested or accepted. If detected, warnings advise users never to disclose them.
3. **Auditing without Leaks**:
   - Inputs are hashed via SHA-256 for duplicate lookup without persisting sensitive user messages verbatim.
