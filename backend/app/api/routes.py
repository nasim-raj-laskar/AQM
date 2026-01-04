from fastapi import APIRouter
from app.schemas.sensor import SensorInput
from app.ml.features import engineer_features
from app.ml.inference import run_inference
from app.db.influx import write_timeseries

router = APIRouter()

@router.post("/infer")
def infer(data: SensorInput):

    features = engineer_features(data.temp, data.hum, data.mq)
    prediction = run_inference(features)

    write_timeseries(
        raw={"temp": data.temp, "hum": data.hum, "mq": data.mq},
        features=features,
        prediction=prediction
    )

    return prediction
