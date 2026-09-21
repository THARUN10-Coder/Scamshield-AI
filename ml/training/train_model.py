import os
import joblib
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix, classification_report
from ml.datasets.generate_data import generate_scam_dataset

def train_and_evaluate():
    dataset_path = "ml/datasets/demo_scam_dataset.csv"
    if not os.path.exists(dataset_path):
        generate_scam_dataset(dataset_path)

    df = pd.read_csv(dataset_path)
    X = df["text"]
    y = df["label"]

    # Stratified Train/Val/Test Split
    X_train, X_temp, y_train, y_temp = train_test_split(X, y, test_size=0.3, random_state=42, stratify=y)
    X_val, X_test, y_val, y_test = train_test_split(X_temp, y_temp, test_size=0.5, random_state=42, stratify=y_temp)

    print(f"Training samples: {len(X_train)}, Validation: {len(X_val)}, Testing: {len(X_test)}")

    # TF-IDF Vectorizer
    vectorizer = TfidfVectorizer(
        ngram_range=(1, 2),
        max_features=1000,
        stop_words="english",
        lowercase=True
    )
    X_train_vec = vectorizer.fit_transform(X_train)
    X_val_vec = vectorizer.transform(X_val)
    X_test_vec = vectorizer.transform(X_test)

    # Classifier
    model = LogisticRegression(C=1.0, solver="liblinear", random_state=42)
    model.fit(X_train_vec, y_train)

    # Evaluation on Test Set
    y_pred = model.predict(X_test_vec)
    y_prob = model.predict_proba(X_test_vec)[:, 1]

    acc = accuracy_score(y_test, y_pred)
    prec = precision_score(y_test, y_pred, zero_division=0)
    rec = recall_score(y_test, y_pred, zero_division=0)
    f1 = f1_score(y_test, y_pred, zero_division=0)
    cm = confusion_matrix(y_test, y_pred).tolist()

    print("\n--- MODEL PERFORMANCE ON DEMO TEST SET ---")
    print(f"Accuracy : {acc:.4f}")
    print(f"Precision: {prec:.4f}")
    print(f"Recall   : {rec:.4f}")
    print(f"F1-Score : {f1:.4f}")
    print("Confusion Matrix:\n", cm)
    print("\nClassification Report:\n", classification_report(y_test, y_pred, zero_division=0))

    # Serialize Artifacts
    os.makedirs("ml/models", exist_ok=True)
    os.makedirs("backend/app/ml/models", exist_ok=True)

    joblib.dump(model, "ml/models/scam_classifier.joblib")
    joblib.dump(vectorizer, "ml/models/tfidf_vectorizer.joblib")
    joblib.dump(model, "backend/app/ml/models/scam_classifier.joblib")
    joblib.dump(vectorizer, "backend/app/ml/models/tfidf_vectorizer.joblib")

    # Save metrics JSON for transparency
    metrics = {
        "model_type": "TF-IDF + Logistic Regression",
        "dataset": "demo_scam_dataset.csv (synthetic demo data for evaluation)",
        "accuracy": acc,
        "precision": prec,
        "recall": rec,
        "f1_score": f1,
        "confusion_matrix": cm
    }
    import json
    with open("ml/models/metrics.json", "w") as f:
        json.dump(metrics, f, indent=2)
    with open("backend/app/ml/models/metrics.json", "w") as f:
        json.dump(metrics, f, indent=2)

    print("Model and vectorizer saved successfully to ml/models/ and backend/app/ml/models/")

if __name__ == "__main__":
    train_and_evaluate()
