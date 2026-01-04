import numpy as np
from app.ml.loader import anomaly_model, aq_model, scaler, FEATURES

AQ_LABELS = {
    0: "Good",
    1: "Moderate",
    2: "Poor",
    3: "Hazardous"
}

def run_inference(features: dict):

    X = np.array([features[f] for f in FEATURES]).reshape(1, -1)

    # Anomaly detection
    X_scaled = scaler.transform(X)
    anomaly_score = float(anomaly_model.decision_function(X_scaled)[0])
    is_anomaly = anomaly_model.predict(X_scaled)[0] == -1

    # AQ classification
    aq_level = int(aq_model.predict(X)[0])
    confidence = float(aq_model.predict_proba(X).max())
    aq_label = AQ_LABELS[aq_level]

    if is_anomaly and aq_level >= 2:
        aq_label = "Hazardous (Anomaly)"

    return {
        "aq_label": aq_label,
        "aq_level": aq_level,
        "confidence": round(confidence, 2),
        "is_anomaly": bool(is_anomaly),
        "anomaly_score": round(anomaly_score, 3)
    }
