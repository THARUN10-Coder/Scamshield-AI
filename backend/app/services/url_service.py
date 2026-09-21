import re
from urllib.parse import urlparse
from typing import Dict, Any, List

class URLScannerService:
    """
    Safely inspects URLs without visiting or querying untrusted remote endpoints.
    Detects structural anomalies, suspicious TLDs, IP hosts, URL shorteners,
    excessive subdomains, typosquatting brand keywords, and credential baiting tokens.
    """

    SUSPICIOUS_TLDS = {
        "xyz", "top", "work", "click", "link", "info", "rest", "buzz", "vip", "cc",
        "tk", "ml", "ga", "cf", "gq", "icu", "club", "surf", "fit", "live", "fun"
    }

    POPULAR_SHORTENERS = {
        "bit.ly", "tinyurl.com", "t.co", "goo.gl", "is.gd", "cutt.ly", "rb.gy", "ow.ly", "bl.ink"
    }

    TARGET_BRANDS = [
        "sbi", "hdfc", "icici", "axis", "kotak", "pnb", "bob", "paytm", "phonepe",
        "googlepay", "gpay", "amazon", "paypal", "netflix", "flipkart", "incometax", "aadhaar"
    ]

    CREDENTIAL_KEYWORDS = [
        "login", "verify", "secure", "update", "banking", "kyc", "signin", "authenticate",
        "refund", "claim", "reward", "password", "wallet", "suspend", "unlock", "confirm"
    ]

    def scan_url(self, raw_url: str) -> Dict[str, Any]:
        url = raw_url.strip()
        if not url.startswith(("http://", "https://")):
            url = "http://" + url

        try:
            parsed = urlparse(url)
        except Exception:
            return self._error_result("Invalid URL structure")

        domain = (parsed.netloc or parsed.path).lower().split(":")[0]
        path = parsed.path.lower()
        protocol = parsed.scheme.lower()

        indicators: List[Dict[str, Any]] = []
        risk_points = 0

        # 1. Protocol: Unencrypted HTTP
        if protocol == "http":
            risk_points += 15
            indicators.append({
                "category": "Insecure Protocol",
                "severity": "MEDIUM",
                "title": "Unencrypted HTTP Protocol",
                "description": "Connection is not secured with HTTPS, exposing transmitted data to eavesdropping."
            })

        # 2. IP Address in Hostname (High indicator of malware/phishing)
        ip_regex = r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$"
        if re.match(ip_regex, domain):
            risk_points += 40
            indicators.append({
                "category": "IP-Based Host",
                "severity": "HIGH",
                "title": "Direct IP Hostname Used",
                "description": f"URL directly uses an IP address ({domain}) rather than a registered domain name."
            })

        # 3. Suspicious TLD
        tld = domain.split(".")[-1] if "." in domain else ""
        if tld in self.SUSPICIOUS_TLDS:
            risk_points += 25
            indicators.append({
                "category": "Suspicious TLD",
                "severity": "MEDIUM",
                "title": f"High-Risk Top Level Domain (.{tld})",
                "description": f"The '.{tld}' extension has a statistically elevated frequency in phishing campaigns."
            })

        # 4. URL Shortener Cloaking
        if domain in self.POPULAR_SHORTENERS:
            risk_points += 25
            indicators.append({
                "category": "URL Shortener",
                "severity": "MEDIUM",
                "title": "URL Shortener Masking",
                "description": "Domain masking hides the true target destination, commonly used to bypass filters."
            })

        # 5. Excessive Subdomains (Domain Spoofing / Subdomain nesting)
        subdomain_parts = domain.split(".")
        if len(subdomain_parts) > 3 and domain not in self.POPULAR_SHORTENERS:
            risk_points += 20
            indicators.append({
                "category": "Domain Spoofing",
                "severity": "MEDIUM",
                "title": "Excessive Subdomains",
                "description": f"Nested subdomain structure ({domain}) often indicates an attempt to deceive users with fake hostnames."
            })

        # 6. Brand Typosquatting / Impersonation in Host or Path
        matched_brands = [b for b in self.TARGET_BRANDS if b in domain and not domain.endswith(f"{b}.com") and not domain.endswith(f"{b}.bank")]
        if matched_brands:
            risk_points += 35
            indicators.append({
                "category": "Brand Impersonation",
                "severity": "HIGH",
                "title": "Brand Keyword in Unofficial Domain",
                "description": f"Domain contains trusted brand names ({', '.join(matched_brands)}) outside official parent domains."
            })

        # 7. Credential / Phishing Keywords in URL
        matched_keywords = [kw for kw in self.CREDENTIAL_KEYWORDS if kw in (domain + path)]
        if matched_keywords:
            risk_points += 20
            indicators.append({
                "category": "Credential Bait",
                "severity": "MEDIUM",
                "title": "Phishing Keywords in URI",
                "description": f"Contains authentication bait keywords: {', '.join(matched_keywords)}"
            })

        # 8. Hyphens in domain (common deceptive pattern e.g., sbi-login-verify)
        if domain.count("-") >= 2:
            risk_points += 15
            indicators.append({
                "category": "Deceptive Naming",
                "severity": "LOW",
                "title": "Multiple Hyphens in Domain",
                "description": "Scammers frequently use hyphenated keywords to mimic authentic domains."
            })

        risk_score = min(100, risk_points)

        if risk_score >= 70:
            risk_level = "HIGH"
            explanation = "This URL exhibits multiple structural attributes characteristic of phishing or deceptive credential harvesting portals."
            recommendation = "Do NOT visit or open this link. Do not enter passwords, OTPs, or banking credentials."
        elif risk_score >= 30:
            risk_level = "MEDIUM"
            explanation = "The URL exhibits ambiguous attributes such as an uncommon TLD, URL shortening, or sensitive keywords."
            recommendation = "Exercise caution before navigating to this page. Verify destination domain authenticity independently."
        else:
            risk_level = "LOW"
            explanation = "No overt structural indicators of phishing, domain spoofing, or deceptive redirection were observed."
            recommendation = "The domain looks standard. Ensure you check for a valid SSL certificate if prompted to sign in."

        confidence = "high" if len(indicators) >= 2 or risk_score >= 70 else "medium"

        return {
            "risk_score": risk_score,
            "risk_level": risk_level,
            "confidence": confidence,
            "indicators": indicators,
            "explanation": explanation,
            "recommendation": recommendation,
            "extracted_metadata": {
                "domain": domain,
                "protocol": protocol,
                "tld": tld,
                "is_ip": bool(re.match(ip_regex, domain)),
                "is_shortener": domain in self.POPULAR_SHORTENERS,
                "brands_detected": matched_brands,
                "keywords_detected": matched_keywords
            }
        }

    def _error_result(self, reason: str) -> Dict[str, Any]:
        return {
            "risk_score": 0,
            "risk_level": "LOW",
            "confidence": "low",
            "indicators": [],
            "explanation": f"Unable to parse URL: {reason}.",
            "recommendation": "Check that the URL is formatted correctly (e.g., https://example.com).",
            "extracted_metadata": {}
        }
