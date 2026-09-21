import io
import re
from urllib.parse import urlparse, parse_qs
from typing import Dict, Any, List
from PIL import Image

class QRScannerService:
    """
    Decodes QR codes safely from uploaded image bytes.
    Analyzes payload type:
    - UPI Payment URI (`upi://pay?...`)
    - Web URL (`http://...`, `https://...`)
    - Plain text / suspicious payload
    Extracts payee parameters safely without initiating payment or connecting to servers.
    """

    def __init__(self):
        self._cv2_detector = None
        self._init_detector()

    def _init_detector(self):
        try:
            import cv2
            self._cv2 = cv2
            self._cv2_detector = cv2.QRCodeDetector()
        except Exception:
            self._cv2 = None
            self._cv2_detector = None

    def decode_and_analyze(self, image_bytes: bytes, filename: str = "") -> Dict[str, Any]:
        # Validate image format and dimensions
        try:
            pil_image = Image.open(io.BytesIO(image_bytes))
            pil_image.verify()
            pil_image = Image.open(io.BytesIO(image_bytes)) # re-open after verify
        except Exception as e:
            return {
                "success": False,
                "error": f"Invalid or corrupted image format: {str(e)}"
            }

        # Attempt decoding
        decoded_text = self._decode_qr(pil_image)

        if not decoded_text:
            return {
                "success": False,
                "error": "We couldn't decode a QR code from this image. Please upload a clear, focused image containing a valid QR code."
            }

        # Analyze decoded payload
        analysis = self._analyze_payload(decoded_text)
        analysis["success"] = True
        return analysis

    def _decode_qr(self, pil_image: Image.Image) -> str:
        # 1. Try OpenCV QRCodeDetector if available
        if self._cv2 is not None and self._cv2_detector is not None:
            try:
                import numpy as np
                # Convert PIL to CV2 BGR
                cv_img = self._cv2.cvtColor(np.array(pil_image.convert("RGB")), self._cv2.COLOR_RGB2BGR)
                val, pts, st_code = self._cv2_detector.detectAndDecode(cv_img)
                if val:
                    return val
            except Exception as e:
                print(f"OpenCV decode error: {e}")

        # 2. Try pyzbar if installed
        try:
            from pyzbar.pyzbar import decode as zbar_decode
            results = zbar_decode(pil_image)
            if results:
                return results[0].data.decode("utf-8")
        except Exception:
            pass

        return ""

    def _analyze_payload(self, payload: str) -> Dict[str, Any]:
        payload_clean = payload.strip()
        indicators: List[Dict[str, Any]] = []
        risk_points = 0
        qr_type = "TEXT"
        metadata: Dict[str, Any] = {"raw_payload": payload_clean}

        # Case 1: UPI Payment URI (upi://pay?pa=...&pn=...)
        if payload_clean.startswith("upi://pay"):
            qr_type = "UPI_PAYMENT"
            parsed = urlparse(payload_clean)
            params = parse_qs(parsed.query)

            # UPI standard query keys
            pa = params.get("pa", [""])[0] # Payee VPA / UPI ID
            pn = params.get("pn", [""])[0] # Payee Name
            am = params.get("am", [""])[0] # Amount
            cu = params.get("cu", ["INR"])[0] # Currency
            tn = params.get("tn", [""])[0] # Transaction Note
            mc = params.get("mc", [""])[0] # Merchant Code

            metadata["payee_upi"] = pa
            metadata["payee_name"] = pn
            metadata["amount"] = am
            metadata["currency"] = cu
            metadata["note"] = tn
            metadata["merchant_code"] = mc

            # Rule: Suspicious recipient name or VPA
            if not pa:
                risk_points += 40
                indicators.append({
                    "category": "Malformed UPI",
                    "severity": "HIGH",
                    "title": "Missing Payee VPA",
                    "description": "The UPI QR contains no valid virtual payment address."
                })
            else:
                # Check for suspicious keywords in VPA handle
                vpa_lower = pa.lower()
                suspicious_keywords = ["refund", "cashback", "lottery", "support", "help", "customer", "officer", "fine", "police"]
                for kw in suspicious_keywords:
                    if kw in vpa_lower:
                        risk_points += 35
                        indicators.append({
                            "category": "Deceptive Payee Handle",
                            "severity": "HIGH",
                            "title": f"Impersonation VPA Keyword ('{kw}')",
                            "description": f"The payee VPA '{pa}' incorporates deceptive keywords simulating official departments."
                        })
                        break

            # Rule: Fixed pre-set high amount
            if am:
                try:
                    amt_float = float(am)
                    if amt_float >= 5000:
                        risk_points += 20
                        indicators.append({
                            "category": "Pre-filled High Amount",
                            "severity": "MEDIUM",
                            "title": f"Fixed Transaction Amount of ₹{amt_float:,.2f}",
                            "description": "Scanning this code will immediately trigger a transfer request for this non-trivial sum."
                        })
                except ValueError:
                    pass

            # Rule: Suspicious note
            if tn:
                tn_lower = tn.lower()
                if any(w in tn_lower for w in ["refund", "reward", "kyc", "block", "verify", "penalty"]):
                    risk_points += 25
                    indicators.append({
                        "category": "Deceptive Note",
                        "severity": "MEDIUM",
                        "title": "Social Engineering Note",
                        "description": f"The note attached to this payment ('{tn}') claims refunds or administrative actions."
                    })

            # Base caution for all payment QR codes
            if risk_points == 0:
                risk_points = 20
                indicators.append({
                    "category": "Payment Transfer Intent",
                    "severity": "LOW",
                    "title": "Outbound Payment QR Code",
                    "description": f"This code will authorize an outbound payment to '{pn or pa}'. Remember that you never need to enter a UPI PIN to receive money."
                })

        # Case 2: Web URL in QR
        elif payload_clean.startswith(("http://", "https://")):
            qr_type = "WEB_URL"
            from app.services.url_service import URLScannerService
            url_scanner = URLScannerService()
            url_res = url_scanner.scan_url(payload_clean)
            risk_points = url_res["risk_score"]
            indicators = url_res["indicators"]
            metadata["url_analysis"] = url_res["extracted_metadata"]

        # Case 3: Other text / phone / raw data
        else:
            qr_type = "PLAIN_TEXT"
            if len(payload_clean) < 4:
                risk_points = 10
            else:
                risk_points = 15

        risk_score = min(100, risk_points)
        if risk_score >= 70:
            risk_level = "HIGH"
            explanation = "This QR code embeds suspicious payment or navigation instructions designed to deceive the payer."
            recommendation = "Do NOT approve this payment or enter your UPI PIN. Never scan a QR code expecting to receive funds."
        elif risk_score >= 30:
            risk_level = "MEDIUM"
            explanation = "The QR code specifies transaction attributes that warrant recipient verification before proceeding."
            recommendation = "Carefully review the payee's name and UPI ID in your banking app before authorizing."
        else:
            risk_level = "LOW"
            explanation = "The QR code has valid structure with no flagged deceptive markers detected."
            recommendation = "Safe to proceed if you recognize the payee. Remember: Receiving money NEVER requires entering your PIN."

        confidence = "high" if qr_type == "UPI_PAYMENT" else "medium"

        return {
            "risk_score": risk_score,
            "risk_level": risk_level,
            "confidence": confidence,
            "indicators": indicators,
            "explanation": explanation,
            "recommendation": recommendation,
            "extracted_metadata": {
                "qr_type": qr_type,
                "payload_snippet": payload_clean[:80] + ("..." if len(payload_clean) > 80 else ""),
                **metadata
            }
        }
