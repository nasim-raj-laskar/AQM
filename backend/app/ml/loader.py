import joblib

anomaly_model = joblib.load("models/anomaly_model.joblib")
aq_model = joblib.load("models/aq_classifier_tree.joblib")
scaler = joblib.load("models/scaler.joblib")
FEATURES = joblib.load("models/features.joblib")
