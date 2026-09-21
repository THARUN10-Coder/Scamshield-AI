import pytest
from app.ml.detectors import NLPFeatureExtractor
from app.services.message_service import MLScamService
from app.services.url_service import URLScannerService
from app.services.phone_service import PhoneScannerService
from app.services.payment_service import PaymentRequestService

def test_nlp_urgency_threat_detection():
    extractor = NLPFeatureExtractor()
    sample = "URGENT! Your SBI bank account will be blocked today. Send OTP immediately."
    features = extractor.extract_features(sample)

    assert features["urgency_detected"] is True
    assert features["threat_detected"] is True
    assert features["credential_request_detected"] is True
    assert features["impersonation_detected"] is True
    assert features["heuristic_score"] >= 70

def test_nlp_benign_message():
    extractor = NLPFeatureExtractor()
    sample = "Your Amazon order has been dispatched and will arrive tomorrow by 6 PM. Track on the app."
    features = extractor.extract_features(sample)

    assert features["threat_detected"] is False
    assert features["credential_request_detected"] is False
    assert features["heuristic_score"] <= 30

def test_ml_message_service_high_risk():
    service = MLScamService()
    sample = "Congratulations! You won Rs 50,000 lottery. Click http://scam-prize.xyz and share your UPI PIN to claim."
    result = service.predict_text(sample)

    assert result["risk_level"] == "HIGH"
    assert result["risk_score"] >= 70
    assert len(result["indicators"]) > 0
    assert "PIN" in result["recommendation"] or "Do NOT" in result["recommendation"]

def test_url_scanner_typosquatting_and_tld():
    scanner = URLScannerService()
    # Phishing bank site with suspicious TLD and hyphenation
    phish_url = "http://sbi-login-update-verify.xyz"
    res = scanner.scan_url(phish_url)

    assert res["risk_level"] in ["HIGH", "MEDIUM"]
    assert res["risk_score"] >= 40
    assert any(ind["category"] == "Suspicious TLD" for ind in res["indicators"])

def test_phone_scanner_foreign_number():
    scanner = PhoneScannerService()
    foreign_phone = "+923001234567"
    res = scanner.scan_phone(foreign_phone)

    assert res["risk_level"] in ["HIGH", "MEDIUM"]
    assert res["risk_score"] >= 40
    assert any(ind["category"] == "Foreign Origin" for ind in res["indicators"])

def test_payment_service_coercion():
    service = PaymentRequestService()
    res = service.analyze_payment(
        recipient="Unknown Merchant",
        amount=8999.0,
        message="Pay immediately or legal warrant will be issued against your bank account."
    )

    assert res["risk_level"] == "HIGH"
    assert res["risk_score"] >= 70
