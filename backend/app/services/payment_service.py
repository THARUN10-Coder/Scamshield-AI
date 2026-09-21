from typing import Dict, Any, List, Optional
from app.ml.detectors import NLPFeatureExtractor

class PaymentRequestService:
    """
    Analyzes structured pre-transaction payment request details:
    Recipient name, amount, note/message context, UPI ID handle, and payment method.
    """

    def __init__(self):
        self.extractor = NLPFeatureExtractor()

    def analyze_payment(
        self,
        recipient: str,
        amount: Optional[float] = None,
        message: Optional[str] = None,
        upi_id: Optional[str] = None,
        phone: Optional[str] = None,
        payment_method: str = "UPI"
    ) -> Dict[str, Any]:
        indicators: List[Dict[str, Any]] = []
        risk_points = 0

        # 1. Analyze contextual message
        if message:
            features = self.extractor.extract_features(message)
            risk_points += int(features["heuristic_score"] * 0.7)
            for flag in features["flag_details"]:
                indicators.append(flag)

        # 2. Recipient Name Analysis
        rec_lower = recipient.lower().strip()
        suspicious_recipients = [
            "unknown merchant", "support desk", "refund officer", "lottery department",
            "telecom department", "customs clearance", "kyc update desk", "helpdesk"
        ]
        if any(sr in rec_lower for sr in suspicious_recipients):
            risk_points += 40
            indicators.append({
                "category": "Suspicious Payee Identity",
                "severity": "HIGH",
                "title": "Impersonated Organization Name",
                "description": f"The recipient name '{recipient}' mimics administrative departments rather than an authenticated merchant."
            })

        # 3. UPI ID handle analysis
        if upi_id:
            upi_lower = upi_id.lower()
            if any(k in upi_lower for k in ["refund", "cashback", "lottery", "support", "help", "officer"]):
                risk_points += 30
                indicators.append({
                    "category": "Deceptive VPA",
                    "severity": "HIGH",
                    "title": "Keyword Spoofing in UPI ID",
                    "description": f"The UPI ID ({upi_id}) uses misleading keywords designed to deceive payers into assuming it is official."
                })

        # 4. Amount analysis
        if amount is not None:
            if amount >= 5000:
                risk_points += 20
                indicators.append({
                    "category": "High Value Transaction",
                    "severity": "MEDIUM",
                    "title": f"High Transaction Amount (₹{amount:,.2f})",
                    "description": "High-value transfers carry severe exposure if directed to unverified parties."
                })
            elif amount < 5 and amount > 0: # 1 rupee scam test
                risk_points += 20
                indicators.append({
                    "category": "Micro-Deposit Test",
                    "severity": "MEDIUM",
                    "title": "Nominal Micro-Amount (Penny Drop)",
                    "description": "Scammers often request ₹1 or ₹10 to link accounts or authorize recurring auto-debit mandates."
                })

        risk_score = min(100, max(0, risk_points))

        if risk_score >= 70:
            risk_level = "HIGH"
            explanation = "This payment request combines coercive context, high-value transfer, or unverified recipient handles characteristic of digital payment fraud."
            recommendation = "Do NOT approve this payment request. Contact the intended party via a verified external channel to confirm validity."
        elif risk_score >= 30:
            risk_level = "MEDIUM"
            explanation = "The payment request has warning signals that warrant manual scrutiny of the recipient before paying."
            recommendation = "Confirm payee identity in your banking app. Verify that the merchant name matches expectations."
        else:
            risk_level = "LOW"
            explanation = "Payment details match standard transaction norms without overt social engineering markers."
            recommendation = "Ensure you know the payee personally or are paying a recognized merchant portal."

        return {
            "risk_score": risk_score,
            "risk_level": risk_level,
            "confidence": "high" if len(indicators) >= 2 else "medium",
            "indicators": indicators,
            "explanation": explanation,
            "recommendation": recommendation,
            "extracted_metadata": {
                "recipient": recipient,
                "amount": amount,
                "upi_id": upi_id,
                "payment_method": payment_method
            }
        }
