from typing import Dict, Any, List, Optional
from app.services.message_service import MLScamService
from app.services.url_service import URLScannerService
from app.services.phone_service import PhoneScannerService
from app.services.payment_service import PaymentRequestService

class MultiSignalFusionEngine:
    """
    Unified AI Risk Engine for Multi-Signal Pre-Transaction Fraud Prevention.
    Aggregates message content, URL characteristics, phone attributes, and payment context
    using configurable weighted scoring, producing an explainable fused assessment.
    """

    def __init__(self):
        self.message_service = MLScamService()
        self.url_service = URLScannerService()
        self.phone_service = PhoneScannerService()
        self.payment_service = PaymentRequestService()

    def fuse_signals(
        self,
        message: Optional[str] = None,
        url: Optional[str] = None,
        phone: Optional[str] = None,
        upi_id: Optional[str] = None,
        amount: Optional[float] = None,
        recipient: Optional[str] = None
    ) -> Dict[str, Any]:
        signals: Dict[str, Any] = {}
        all_indicators: List[Dict[str, Any]] = []
        weighted_sum = 0.0
        total_weight = 0.0

        # 1. Message Signal
        if message and message.strip():
            msg_res = self.message_service.predict_text(message)
            signals["message"] = msg_res
            weight = 0.35
            weighted_sum += msg_res["risk_score"] * weight
            total_weight += weight
            all_indicators.extend(msg_res["indicators"])

        # 2. URL Signal
        if url and url.strip():
            url_res = self.url_service.scan_url(url)
            signals["url"] = url_res
            weight = 0.25
            weighted_sum += url_res["risk_score"] * weight
            total_weight += weight
            all_indicators.extend(url_res["indicators"])

        # 3. Phone Signal
        if phone and phone.strip():
            phone_res = self.phone_service.scan_phone(phone, context=message or "")
            signals["phone"] = phone_res
            weight = 0.20
            weighted_sum += phone_res["risk_score"] * weight
            total_weight += weight
            all_indicators.extend(phone_res["indicators"])

        # 4. Payment Context Signal
        if recipient or amount or upi_id:
            pay_res = self.payment_service.analyze_payment(
                recipient=recipient or "Unknown",
                amount=amount,
                message=message,
                upi_id=upi_id,
                phone=phone
            )
            signals["payment"] = pay_res
            weight = 0.20
            weighted_sum += pay_res["risk_score"] * weight
            total_weight += weight
            # Avoid duplicate indicators if message was already analyzed
            if not message:
                all_indicators.extend(pay_res["indicators"])

        # Calculate final fused score
        if total_weight > 0:
            fused_score = int(weighted_sum / total_weight)
        else:
            fused_score = 0

        # Apply synergy escalation: if both message AND url are flagged, escalate risk
        has_high_msg = signals.get("message", {}).get("risk_level") == "HIGH"
        has_high_url = signals.get("url", {}).get("risk_level") == "HIGH"
        if has_high_msg and has_high_url:
            fused_score = max(fused_score, 88)

        fused_score = max(0, min(100, fused_score))

        if fused_score >= 70:
            risk_level = "HIGH"
            explanation = "Cross-signal fusion detected severe correlated fraud indicators across communication context, URL parameters, and payment vectors."
            recommendation = "HALT TRANSACTION IMMEDIATELY. Do not transfer funds, scan codes, or enter PIN. Contact official bank support independently."
        elif fused_score >= 30:
            risk_level = "MEDIUM"
            explanation = "Multiple moderate risk signals detected across submitted channels that require sender authentication."
            recommendation = "Verify identity with the sender through an out-of-band channel before completing payment."
        else:
            risk_level = "LOW"
            explanation = "Multi-signal analysis indicates standard, benign interaction attributes without identified deception tactics."
            recommendation = "Safe to proceed under normal precautions. Remember to never share authorization OTPs."

        return {
            "risk_score": fused_score,
            "risk_level": risk_level,
            "confidence": "high" if len(signals) >= 2 else "medium",
            "indicators": all_indicators,
            "explanation": explanation,
            "recommendation": recommendation,
            "extracted_metadata": {
                "active_signal_count": len(signals),
                "signals_evaluated": list(signals.keys()),
                "individual_scores": {k: v.get("risk_score", 0) for k, v in signals.items()}
            }
        }
