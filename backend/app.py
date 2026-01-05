from fastapi import FastAPI            #type:ignore
from pydantic import BaseModel         #type:ignore
from ml import run_inference
from db import write_to_influx

app = FastAPI(title="Air Quality Backend")

#Input schema
class SensorInput(BaseModel):
    temp: float
    hum: float
    mq: float

AQ_LABELS = {
    0: "Good",
    1: "Moderate",
    2: "Poor",
    3: "Hazardous"
}

#Inference endpoint
@app.post("/infer")
def infer(data: SensorInput):

    feats, aq_level, confidence, anomaly, anomaly_score = run_inference(
        data.temp, data.hum, data.mq
    )

    #write
    write_to_influx(
        data.temp,
        data.hum,
        data.mq,
        feats,
        aq_level,
        confidence,
        anomaly,
        anomaly_score
    )

    #Response for ESP32
    return {
        "temp": data.temp,
        "hum": data.hum,
        "aq_label": AQ_LABELS[aq_level],
        "anomaly": bool(anomaly)
    }
