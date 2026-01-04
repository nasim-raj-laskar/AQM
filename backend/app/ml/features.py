import numpy as np
from app.core.state import mq_buffer

def engineer_features(temp: float, hum: float, mq: float):

    mq_buffer.append(mq)

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
