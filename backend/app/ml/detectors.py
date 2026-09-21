import re
from typing import Dict, Any, List

class NLPFeatureExtractor:
    """
    Explainable NLP Feature Detector for digital payment scam indicators.
    Detects urgency, threat, reward, credential requests, payment solicitations,
    and impersonation patterns with exact matches and contextual heuristics.
    """

    PATTERNS = {
        "urgency": [
            r"\b(immediately|urgent|urgently|hurry|act now|right now|limited time|expires in|within \d+ (hours?|mins?|minutes?)|valid only today|last chance|instant)\b"
        ],
        "threat": [
            r"\b(account.*(blocked|suspended|deactivated|frozen|terminated)|legal action|police|court|fined?|penalty|arrest|electricity.*(cut|disconnect|power)|service stopped|kyc.*(expired|pending|incomplete))\b"
        ],
        "reward": [
            r"\b(congratulations|you (have )?won|winner|cashback|cash prize|lottery|lucky draw|free gift|reward point|jackpot|claim ₹?\d+)\b"
        ],
        "credential_request": [
            r"\b(otp|one time password|pin|upi pin|atm pin|cvv|password|passcode|banking details|net banking|card number|secret code)\b"
        ],
        "payment_request": [
            r"\b(send money|pay now|pay immediately|transfer (₹?\d+|amount)|scan qr|click to pay|deposit|processing fee|refund fee|registration fee)\b"
        ],
        "impersonation": [
            r"\b(sbi|hdfc|icici|axis|rbi|reserve bank|paytm|phonepe|google pay|gpay|amazon pay|electricity board|bescom|tneb|wbseb|uppcl|customer care|helpline|support team|tech support|official support)\b"
        ],
        "suspicious_links": [
            r"https?://[^\s<>\"']+",
            r"\b[a-zA-Z0-9.-]+\.(top|xyz|tk|ml|ga|cf|gq|work|click|link|info|rest|buzz|vip|cc)\b",
            r"\b(bit\.ly|tinyurl\.com|t\.co|goo\.gl|is\.gd|cutt\.ly)/[a-zA-Z0-9_-]+"
        ]
    }

    def extract_features(self, text: str) -> Dict[str, Any]:
        text_lower = text.lower()
        extracted = {}
        total_flags = 0
        flag_details = []

        # 1. Urgency
        urgency_matches = []
        for p in self.PATTERNS["urgency"]:
            matches = re.findall(p, text_lower, re.IGNORECASE)
            if matches:
                urgency_matches.extend([m[0] if isinstance(m, tuple) else m for m in matches])
        extracted["urgency_detected"] = len(urgency_matches) > 0
        extracted["urgency_matches"] = list(set(urgency_matches))
        if extracted["urgency_detected"]:
            total_flags += 1.5
            flag_details.append({
                "category": "Urgency",
                "severity": "HIGH",
                "title": "High Urgency & Pressure",
                "description": f"Message induces artificial time panic using terms: {', '.join(extracted['urgency_matches'])}"
            })

        # 2. Threat & Coercion
        threat_matches = []
        for p in self.PATTERNS["threat"]:
            matches = re.findall(p, text_lower, re.IGNORECASE)
            if matches:
                threat_matches.extend([m[0] if isinstance(m, tuple) else m for m in matches])
        extracted["threat_detected"] = len(threat_matches) > 0
        extracted["threat_matches"] = list(set(threat_matches))
        if extracted["threat_detected"]:
            total_flags += 2.0
            flag_details.append({
                "category": "Threat / Coercion",
                "severity": "HIGH",
                "title": "Account Block / Service Suspension Threat",
                "description": f"Uses fear tactics warning of punitive actions or disconnection: {', '.join(extracted['threat_matches'])}"
            })

        # 3. Reward / Lottery Bait
        reward_matches = []
        for p in self.PATTERNS["reward"]:
            matches = re.findall(p, text_lower, re.IGNORECASE)
            if matches:
                reward_matches.extend([m[0] if isinstance(m, tuple) else m for m in matches])
        extracted["reward_detected"] = len(reward_matches) > 0
        extracted["reward_matches"] = list(set(reward_matches))
        if extracted["reward_detected"]:
            total_flags += 1.5
            flag_details.append({
                "category": "Reward Bait",
                "severity": "MEDIUM",
                "title": "Unrealistic Financial Prize or Reward",
                "description": "Lures user with lottery, prize, or unsolicited financial claims."
            })

        # 4. Credential / Sensitive Data Solicitation
        cred_matches = []
        for p in self.PATTERNS["credential_request"]:
            matches = re.findall(p, text_lower, re.IGNORECASE)
            if matches:
                cred_matches.extend([m[0] if isinstance(m, tuple) else m for m in matches])
        extracted["credential_request_detected"] = len(cred_matches) > 0
        extracted["credential_matches"] = list(set(cred_matches))
        if extracted["credential_request_detected"]:
            total_flags += 3.0  # Critical danger
            flag_details.append({
                "category": "Credential Solicitation",
                "severity": "HIGH",
                "title": "Requests Sensitive Banking Information",
                "description": f"Directly asks for protected secrets ({', '.join(extracted['credential_matches'])}) which legitimate entities never request."
            })

        # 5. Payment Demand
        pay_matches = []
        for p in self.PATTERNS["payment_request"]:
            matches = re.findall(p, text_lower, re.IGNORECASE)
            if matches:
                pay_matches.extend([m[0] if isinstance(m, tuple) else m for m in matches])
        extracted["payment_request_detected"] = len(pay_matches) > 0
        extracted["payment_matches"] = list(set(pay_matches))
        if extracted["payment_request_detected"]:
            total_flags += 1.2
            flag_details.append({
                "category": "Payment Prompt",
                "severity": "MEDIUM",
                "title": "Pre-Transaction Money Demand",
                "description": "Prompts recipient to transfer money or scan a QR code under suspicious pretext."
            })

        # 6. Impersonation
        impersonation_matches = []
        for p in self.PATTERNS["impersonation"]:
            matches = re.findall(p, text_lower, re.IGNORECASE)
            if matches:
                impersonation_matches.extend([m[0] if isinstance(m, tuple) else m for m in matches])
        extracted["impersonation_detected"] = len(impersonation_matches) > 0
        extracted["impersonation_matches"] = list(set(impersonation_matches))
        if extracted["impersonation_detected"]:
            total_flags += 1.0
            flag_details.append({
                "category": "Impersonation",
                "severity": "MEDIUM",
                "title": "Brand or Institutional Impersonation",
                "description": f"Claims to represent recognized entities: {', '.join(extracted['impersonation_matches'])}"
            })

        # 7. Embedded Links / Shorteners
        links = []
        for p in self.PATTERNS["suspicious_links"]:
            found = re.findall(p, text, re.IGNORECASE)
            if found:
                links.extend([f[0] if isinstance(f, tuple) else f for f in found])
        extracted["links_found"] = list(set(links))
        if extracted["links_found"]:
            total_flags += 1.5
            flag_details.append({
                "category": "Unverified Link",
                "severity": "MEDIUM",
                "title": "External Action URL",
                "description": f"Directs target to external link(s): {', '.join(extracted['links_found'][:2])}"
            })

        # Heuristic Risk Calculation (0 to 100)
        heuristic_score = min(100, int((total_flags / 7.5) * 100))
        extracted["heuristic_score"] = heuristic_score
        extracted["flag_details"] = flag_details
        extracted["total_flags"] = total_flags

        return extracted
