import os
import pandas as pd                       #type:ignore
import numpy as np
import joblib
import matplotlib.pyplot as plt

from sklearn.ensemble import IsolationForest
from sklearn.tree import DecisionTreeClassifier, plot_tree
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.preprocessing import StandardScaler

# CONFIG
DATA_PATH = "../dataset/air_quality.csv"
MODEL_DIR = "models"
OUTPUT_DIR = "outputs"

FEATURES = [
    "gas_norm",
    "rolling_mean_10",
    "rolling_std_10",
    "gas_diff",
    "gas_diff_norm",
    "hum_adjusted_gas",
    "temp_hum",
    "temp_gas",
    "hum_gas"
]

CLASS_NAMES = ["Good", "Moderate", "Poor", "Hazardous"]

os.makedirs(MODEL_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

# LOAD & CLEAN DATA
print("\n🔹 Loading dataset...")
df = pd.read_csv(DATA_PATH)

# Drop NaNs caused by rolling / diff features
df = df.dropna().reset_index(drop=True)

X = df[FEATURES]

# AQ LABELING (Heuristic)
def air_quality_label(mq):
    if mq < 220:
        return 0  # Good
    elif mq < 260:
        return 1  # Moderate
    elif mq < 300:
        return 2  # Poor
    else:
        return 3  # Hazardous

df["aq_label"] = df["mq"].apply(air_quality_label)
y = df["aq_label"]

#ANOMALY DETECTION (Isolation Forest)
print("\n🔹 Training Anomaly Detection Model...")

#Train only on NORMAL air 
normal_df = df[df["mq"] < 260]
X_anomaly = normal_df[FEATURES]

# Scale features 
scaler = StandardScaler()
X_anomaly_scaled = scaler.fit_transform(X_anomaly)

anomaly_model = IsolationForest(
    n_estimators=300,
    contamination=0.01,
    random_state=42
)

anomaly_model.fit(X_anomaly_scaled)

#Save anomaly artifacts
joblib.dump(anomaly_model, f"{MODEL_DIR}/anomaly_model.joblib")
joblib.dump(scaler, f"{MODEL_DIR}/scaler.joblib")

print("Anomaly model saved")

# Anomaly Evaluation
X_all_scaled = scaler.transform(df[FEATURES])

df["anomaly_score"] = anomaly_model.decision_function(X_all_scaled)
df["is_anomaly"] = anomaly_model.predict(X_all_scaled)  # -1 = anomaly

total = len(df)
anomalies = (df["is_anomaly"] == -1).sum()

print("\n Anomaly Detection Summary")
print(f"Total samples       : {total}")
print(f"Detected anomalies  : {anomalies}")
print(f"Anomaly percentage  : {anomalies / total * 100:.2f}%")

print("\n AQ distribution among anomalies:")
print(
    df[df["is_anomaly"] == -1]["aq_label"]
    .value_counts()
    .sort_index()
)

#Plot anomaly score distribution
plt.figure(figsize=(10, 4))
plt.hist(df["anomaly_score"], bins=50)
plt.xlabel("Anomaly Score")
plt.ylabel("Frequency")
plt.title("Isolation Forest Anomaly Score Distribution")
plt.tight_layout()
plt.savefig(f"{OUTPUT_DIR}/anomaly_score_distribution.png", dpi=300)
plt.show()

#AQ CLASSIFICATION (Decision Tree)
print("\n🔹 Training AQ classifier (Decision Tree)...")

X_train, X_val, y_train, y_val = train_test_split(
    X, y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

model = DecisionTreeClassifier(
    max_depth=5,
    min_samples_leaf=30,
    random_state=42
)

model.fit(X_train, y_train)

#Evaluation
y_pred = model.predict(X_val)
y_prob = model.predict_proba(X_val)

print("\nClassification Report:")
print(classification_report(y_val, y_pred, target_names=CLASS_NAMES))

print("\nConfusion Matrix:")
print(confusion_matrix(y_val, y_pred))

#Confidence analysis
pred_df = pd.DataFrame({
    "True_Label": y_val.values,
    "Pred_Label": y_pred,
    "Confidence": y_prob.max(axis=1)
})

print("\nSample predictions with confidence:")
print(pred_df.head(10))

low_conf = pred_df[pred_df["Confidence"] < 0.6]
print(f"\nLow-confidence predictions (<0.6): {len(low_conf)}")

#Decision Tree Visualization
plt.figure(figsize=(22, 10))
plot_tree(
    model,
    feature_names=FEATURES,
    class_names=CLASS_NAMES,
    filled=True,
    rounded=True,
    fontsize=9
)
plt.title("Decision Tree for Air Quality Classification")
plt.tight_layout()
plt.savefig(f"{OUTPUT_DIR}/aq_decision_tree.png", dpi=300)
plt.show()

#Save Artifacts
joblib.dump(model, f"{MODEL_DIR}/aq_classifier_tree.joblib")
joblib.dump(FEATURES, f"{MODEL_DIR}/features.joblib")

print("\nDecision Tree AQ classifier saved")
print("Training complete")
