# ScamShield AI — Explainable Pre-Transaction Digital Payment Fraud Prevention

[![FastAPI](https://img.shields.io/badge/FastAPI-0.110.0-009688.svg?style=flat&logo=FastAPI&logoColor=white)](https://fastapi.tiangolo.com)
[![React](https://img.shields.io/badge/React-18-61DAFB.svg?style=flat&logo=React&logoColor=black)](https://react.dev)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.0-blue.svg?style=flat&logo=TypeScript&logoColor=white)](https://www.typescriptlang.org)
[![scikit-learn](https://img.shields.io/badge/scikit--learn-1.4+-F7931E.svg?style=flat&logo=scikitlearn&logoColor=white)](https://scikit-learn.org)
[![TailwindCSS](https://img.shields.io/badge/Tailwind_CSS-3.4-38B2AC.svg?style=flat&logo=tailwind-css&logoColor=white)](https://tailwindcss.com)

> **ScamShield AI** protects users **BEFORE** they make a payment by analyzing suspicious SMS/messages, phishing links, UPI QR codes, customer-care phone numbers, and payment requests with explainable AI.

---

## 🌟 Key Features

1. **Pre-Transaction Fraud Interception**: Evaluates suspicious signals before authorization or money transfer.
2. **Explainable AI (XAI)**: Never returns a black-box answer. Provides clear, itemized detection indicators, threat categorizations, and plain-language action guidance.
3. **Multi-Signal Scan Center**:
   - 📱 **SMS / Text Scanner**: ML (TF-IDF + Logistic Regression) + NLP heuristics for urgency, threat, prize lure, and credential requests.
   - 🌐 **Static URL Inspector**: Safe offline structural parsing for IP hosts, typosquatting, shorteners, and high-risk TLDs.
   - 📷 **Safe QR Decoder**: Extracts UPI payment parameters (`upi://pay`) and validates recipient VPAs without initiating transfers.
   - 📞 **Phone & Support Caller Scanner**: Identifies foreign call prefixes and personal mobile numbers pretending to be official customer care.
   - 💳 **Payment Request Analyzer**: Evaluates payee handles, transfer amounts, and coercion contexts.
   - 🖼️ **Screenshot Scanner**: OCR-assisted pipeline for chats and payment dialogues.
4. **Interactive Dashboard & Audit History**: Visual charts (Recharts) showing risk distributions, vector breakdown, and privacy-preserving audit logs.
5. **Community Telemetry & Safety Center**: Crowdsourced reporting and educational guides on UPI and digital banking hygiene.

---

## 🚀 Quick Start Guide

### Prerequisites
- **Python 3.10+** (tested on Python 3.13)
- **Node.js 18+** & **npm**

---

### Step 1: Start Backend API

```powershell
# Navigate to backend directory
cd backend

# Install dependencies
py -m pip install -r requirements.txt

# (Optional) Train/re-train ML model
$env:PYTHONPATH="."
py ../ml/training/train_model.py

# Run FastAPI backend server
py main.py
```

- API Server will be accessible at: `http://127.0.0.1:8000`
- Interactive OpenAPI / Swagger Documentation: `http://127.0.0.1:8000/docs`

---

### Step 2: Start Frontend Application

```powershell
# In a new terminal, navigate to frontend directory
cd frontend

# Install packages
npm install

# Start Vite development server
npm run dev
```

- Web UI will be accessible at: `http://localhost:5173`

---

## 🧪 Running Automated Tests

```powershell
cd backend
$env:PYTHONPATH="."
py -m pytest tests/test_scam_engine.py -v
```

All 6 test cases for NLP detection, ML classification, URL analysis, phone vetting, and payment scoring will execute and validate.

---

## 📁 Repository Structure

```
scamshield/
├── backend/
│   ├── app/
│   │   ├── api/v1/          # REST API endpoints (Auth, Scans, History, Stats)
│   │   ├── core/            # Config, DB connection, Settings
│   │   ├── models/          # SQLAlchemy DB models (User, Scan, Detail, Report)
│   │   ├── schemas/         # Pydantic validation schemas
│   │   ├── services/        # Scan services (Message, URL, QR, Phone, Payment)
│   │   ├── ml/              # NLP detectors and trained models
│   │   └── security/        # JWT auth and password hashing
│   ├── tests/               # Pytest suite
│   ├── main.py              # Application entrypoint
│   └── requirements.txt
│
├── frontend/
│   ├── src/
│   │   ├── components/      # ScanCenter, RiskBadge, RiskResultModal
│   │   ├── pages/           # Dashboard, History, Report, SafetyCenter
│   │   ├── services/        # Frontend API client
│   │   ├── types/           # TypeScript definitions
│   │   ├── App.tsx          # Main App shell & responsive sidebar
│   │   └── index.css        # Tailwind & glassmorphism theme
│   ├── tailwind.config.js
│   └── package.json
│
├── ml/
│   ├── datasets/            # Training data & generator
│   └── training/            # Model training and evaluation script
│
├── docs/
│   ├── architecture.md      # Architectural design & data flow
│   └── demo.md              # 5-minute hackathon pitch & scenario walkthrough
│
└── README.md
```

---

## 🛡️ Important Safety & Ethical Principles

ScamShield AI is an intentionally defensive tool:
- It **never** requests or stores bank account passwords, UPI PINs, ATM PINs, card CVVs, or OTPs.
- It **never** visits or queries untrusted remote links during scanning.
- Output metrics are formulated as **Risk Scores** rather than statistical certainties to encourage critical user judgment.
