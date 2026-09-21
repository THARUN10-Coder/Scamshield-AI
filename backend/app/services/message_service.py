import os
import joblib
from typing import Dict, Any, Tuple
from app.ml.detectors import NLPFeatureExtractor
from app.core.config import settings

class MLScamService:
    def __init__(self):
        self.extractor = NLPFeatureExtractor()
        self.model = None
        self.vectorizer = None
        self._load_models()

    def _load_models(self):
        model_path = os.path.join(settings.ML_MODEL_PATH, "scam_classifier.joblib")
        vec_path = os.path.join(settings.ML_MODEL_PATH, "tfidf_vectorizer.joblib")

        if os.path.exists(model_path) and os.path.exists(vec_path):
            try:
                self.model = joblib.load(model_path)
                self.vectorizer = joblib.load(vec_path)
            except Exception as e:
                print(f"Warning: Error loading ML model: {e}")
        else:
            print(f"ML model artifacts not found at {model_path}. Using heuristic rule engine fallback.")

    def predict_text(self, text: str) -> Dict[str, Any]:
        # 1. Heuristic feature extraction
        heuristic = self.extractor.extract_features(text)
        
        # 2. ML model prediction
        ml_prob = 0.0
        ml_available = False
        if self.model and self.vectorizer:
            try:
                vec = self.vectorizer.transform([text])
                probs = self.model.predict_proba(vec)[0]
                ml_prob = float(probs[1]) # probability of scam class
                ml_available = True
            except Exception as e:
                print(f"ML inference error: {e}")

        # 3. Explainable Fusion Score (0-100)
        # Combine heuristic signals with ML prediction
        heuristic_score = heuristic["heuristic_score"]
        if ml_available:
            ml_score = int(ml_prob * 100)
            # 60% rule indicators (exact triggers) + 40% statistical ML prediction
            combined_score = int((0.60 * heuristic_score) + (0.40 * ml_score))
        else:
            combined_score = heuristic_score

        # Clamp between 0 and 100
        risk_score = max(0, min(100, combined_score))

        # Categorize Risk Level
        if risk_score >= settings.HIGH_RISK_THRESHOLD:
            risk_level = "HIGH"
        elif risk_score >= settings.LOW_RISK_THRESHOLD:
            risk_level = "MEDIUM"
        else:
            risk_level = "LOW"

        # Determine confidence
        indicator_count = len(heuristic["flag_details"])
        if indicator_count >= 3 or (ml_available and (ml_prob > 0.85 or ml_prob < 0.15)):
            confidence = "high"
        elif indicator_count >= 1 or ml_available:
            confidence = "medium"
        else:
            confidence = "low"

        # Generate Explainable Justification & Recommendation
        explanation, recommendation = self._generate_explanation(heuristic, risk_level, risk_score)

        return {
            "risk_score": risk_score,
            "risk_level": risk_level,
            "confidence": confidence,
            "indicators": heuristic["flag_details"],
            "explanation": explanation,
            "recommendation": recommendation,
            "extracted_metadata": {
                "ml_probability": round(ml_prob, 3) if ml_available else None,
                "heuristic_score": heuristic_score,
                "urgency_matches": heuristic.get("urgency_matches", []),
                "threat_matches": heuristic.get("threat_matches", []),
                "credential_matches": heuristic.get("credential_matches", []),
                "impersonation_matches": heuristic.get("impersonation_matches", []),
                "links_found": heuristic.get("links_found", [])
            }
        }

    def _generate_explanation(self, heuristic: Dict[str, Any], risk_level: str, score: int) -> Tuple[str, str]:
        flags = heuristic["flag_details"]
        if risk_level == "HIGH":
            reasons = []
            if heuristic.get("credential_request_detected"):
                reasons.append("solicitation of confidential banking credentials/OTP")
            if heuristic.get("threat_detected"):
                reasons.append("threats of service termination or legal enforcement")
            if heuristic.get("urgency_detected"):
                reasons.append("artificial urgency designed to induce panic")
            if heuristic.get("impersonation_detected"):
                reasons.append("unverified claims representing legitimate institutions")

            reason_str = ", ".join(reasons) if reasons else "multiple high-risk fraudulent patterns"
            explanation = f"This message exhibits critical warning signs typical of social engineering scams, including {reason_str}."
            recommendation = "Do NOT click any provided links, do NOT dial the mentioned numbers, and NEVER disclose OTPs, PINs, or passwords. Verify notifications exclusively through the bank or entity's official portal."
        elif risk_level == "MEDIUM":
            explanation = "The content contains suspicious phrases or unusual requests commonly observed in promotional clickbaits, lottery lures, or unverified claims."
            recommendation = "Exercise caution. Do not forward money, provide personal details, or grant remote access. Cross-verify the claim via recognized channels."
        else:
            explanation = "No overt fraudulent patterns, credential phishing requests, or coercive threats were detected in the analyzed message."
            recommendation = "The content appears safe based on structural analysis. Always remain vigilant and never share UPI PINs or OTPs even if prompted later."

        return explanation, recommendation
