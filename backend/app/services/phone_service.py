import re
from typing import Dict, Any, List

class PhoneScannerService:
    """
    Analyzes phone numbers and customer-care contacts for suspicious formatting,
    toll-free customer service spoofing, high-risk country codes, and known scam patterns.
    Adheres strictly to safe, measured cybersecurity phrasing.
    """

    # Well-known telecom / bank genuine toll-free prefixes in India: 1800, 1909
    # Scammers frequently provide standard 10-digit mobile numbers (+91-9xxx or 8xxx)
    # claiming to be "official customer care" of multinational companies or banks.
    
    KNOWN_SCAM_PATTERNS = [
        r"^(?:\+91|91)?[6-9]\d{9}$" # standard mobile pretending to be customer care
    ]

    HIGH_RISK_COUNTRY_PREFIXES = {
        "+92": "Pakistan",
        "+880": "Bangladesh",
        "+234": "Nigeria",
        "+254": "Kenya",
        "+855": "Cambodia",
        "+95": "Myanmar"
    }

    def scan_phone(self, raw_phone: str, context: str = "") -> Dict[str, Any]:
        cleaned = re.sub(r"[\s\-\(\)]", "", raw_phone)
        indicators: List[Dict[str, Any]] = []
        risk_points = 0

        # 1. International code check
        detected_country = "Domestic / Standard"
        is_foreign = False
        for prefix, country in self.HIGH_RISK_COUNTRY_PREFIXES.items():
            if cleaned.startswith(prefix):
                detected_country = country
                is_foreign = True
                risk_points += 45
                indicators.append({
                    "category": "Foreign Origin",
                    "severity": "HIGH",
                    "title": f"International Calling Code ({prefix} - {country})",
                    "description": f"Frequently observed in overseas social engineering and lottery scams targeting domestic users."
                })
                break

        # 2. Check customer-care context vs mobile number format
        is_toll_free = cleaned.startswith("1800") or cleaned.startswith("+1800") or cleaned.startswith("1909")
        is_mobile_length = (len(cleaned) == 10 and cleaned[0] in "6789") or (cleaned.startswith("+91") and len(cleaned) == 13)

        if "customer care" in context.lower() or "support" in context.lower() or "helpline" in context.lower():
            if is_mobile_length and not is_toll_free:
                risk_points += 35
                indicators.append({
                    "category": "Customer Care Impersonation",
                    "severity": "HIGH",
                    "title": "Personal Mobile Number Claiming to be Customer Care",
                    "description": "Legitimate banks and corporate entities rarely publish individual personal mobile numbers as their primary support lines."
                })

        # 3. Repeating / suspicious digits pattern (e.g., 9999999999 or sequential 1234567890)
        digits_only = re.sub(r"\D", "", cleaned)
        if len(digits_only) >= 8:
            if len(set(digits_only)) <= 2:
                risk_points += 30
                indicators.append({
                    "category": "Number Pattern Anomaly",
                    "severity": "MEDIUM",
                    "title": "Repetitive Digit Sequence",
                    "description": "The number uses repetitive mock digits often used in placeholder or fraudulent listings."
                })

        # Base informational score
        if risk_points == 0:
            risk_points = 10
            indicators.append({
                "category": "Standard Formatting",
                "severity": "LOW",
                "title": "Standard Format Recognized",
                "description": "The phone string matches typical domestic dialing patterns."
            })

        risk_score = min(100, risk_points)

        if risk_score >= 70:
            risk_level = "HIGH"
            explanation = "This contact number shows characteristics frequently correlated with customer-care impersonation or fraudulent listings."
            recommendation = "Do NOT call this number. Find the genuine contact helpline exclusively from the organization's verified official website or mobile app."
        elif risk_score >= 30:
            risk_level = "MEDIUM"
            explanation = "Potentially suspicious based on available dialing indicators and context."
            recommendation = "Verify the caller or recipient independently before sharing information or making payments."
        else:
            risk_level = "LOW"
            explanation = "No overt anomaly or known malicious spoofing pattern detected from the phone format."
            recommendation = "Always exercise discretion when answering calls requesting OTP or financial transfers."

        return {
            "risk_score": risk_score,
            "risk_level": risk_level,
            "confidence": "medium",
            "indicators": indicators,
            "explanation": explanation,
            "recommendation": recommendation,
            "extracted_metadata": {
                "raw_phone": raw_phone,
                "cleaned_phone": cleaned,
                "detected_region": detected_country,
                "is_toll_free": is_toll_free,
                "is_mobile_format": is_mobile_length
            }
        }
