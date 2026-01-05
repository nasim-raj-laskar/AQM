import joblib
import numpy as np

#load ML models
anomaly_model = joblib.load("models/anomaly_model.joblib")
aq_model = joblib.load("models/aq_classifier_tree.joblib")
scaler = joblib.load("models/scaler.joblib")
FEATURES = joblib.load("models/features.joblib")

#Rolling buffer
WINDOW = 10
mq_buffer = []

#Feature engineering
def engineer_features(temp, hum, mq):
    mq_buffer.append(mq)
    if len(mq_buffer) > WINDOW:
        mq_buffer.pop(0)

    rolling_mean = float(np.mean(mq_buffer))
    rolling_std = float(np.std(mq_buffer))
    gas_diff = mq_buffer[-1] - mq_buffer[-2] if len(mq_buffer) > 1 else 0.0

    return {
        "gas_norm": mq / (temp * hum + 1),
        "rolling_mean_10": rolling_mean,
        "rolling_std_10": rolling_std,
        "gas_diff": gas_diff,
        "gas_diff_norm": gas_diff / (mq + 1e-5),
        "hum_adjusted_gas": mq * (1 + hum / 100),
        "temp_hum": temp * hum,
        "temp_gas": temp * mq,
        "hum_gas": hum * mq
    }

def run_inference(temp, hum, mq):
    feats = engineer_features(temp, hum, mq)
    X = np.array([feats[f] for f in FEATURES]).reshape(1, -1)

    # Anomaly detection
    X_scaled = scaler.transform(X)
    anomaly_score = float(anomaly_model.decision_function(X_scaled)[0])
    is_anomaly = bool(anomaly_model.predict(X_scaled)[0] == -1)

    # AQ classification
    aq_level = int(aq_model.predict(X)[0])
    confidence = float(aq_model.predict_proba(X).max())

    return feats, aq_level, confidence, is_anomaly, anomaly_score

