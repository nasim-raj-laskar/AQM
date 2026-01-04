import pandas as pd                   #type:ignore
import numpy as np

# Load JSONL directly
df = pd.read_json("../dataset/raw.jsonl", lines=True)

# Ensure numeric
cols = ["mq", "temp", "hum", "ts"]
df[cols] = df[cols].apply(pd.to_numeric, errors="coerce")

# Sort by timestamps
df = df.sort_values("ts").reset_index(drop=True)

# Feature Engineering
# Normalized gas value
df["gas_norm"] = df["mq"] / (df["temp"] * df["hum"] + 1)

# Rolling statistics
WINDOW = 10
df["rolling_mean_10"] = df["mq"].rolling(WINDOW).mean()
df["rolling_std_10"]  = df["mq"].rolling(WINDOW).std()

# Rate of change
df["gas_diff"] = df["mq"].diff()
df["gas_diff_norm"] = df["gas_diff"] / (df["mq"].shift(1) + 1e-5)

# Humidity adjusted index
df["hum_adjusted_gas"] = df["mq"] * (1 + df["hum"] / 100)

# Interaction features
df["temp_hum"] = df["temp"] * df["hum"]
df["temp_gas"] = df["temp"] * df["mq"]
df["hum_gas"]  = df["hum"] * df["mq"]

#NaNs
df = df.dropna().reset_index(drop=True)

#Save processed data
df.to_csv("../dataset/air_quality.csv", index=False)

print("Feature engineering complete")
print(df.head())
