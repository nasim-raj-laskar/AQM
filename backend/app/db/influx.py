import time
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS
from app.core.config import INFLUX_URL, INFLUX_TOKEN, INFLUX_ORG, INFLUX_BUCKET

client = InfluxDBClient(
    url=INFLUX_URL,
    token=INFLUX_TOKEN,
    org=INFLUX_ORG
)

write_api = client.write_api(write_options=SYNCHRONOUS)

def write_timeseries(raw: dict, features: dict, prediction: dict):

    ts = int(time.time() * 1e9)

    point = (
        Point("air_quality")
        .time(ts)
        .field("temp", raw["temp"])
        .field("hum", raw["hum"])
        .field("mq", raw["mq"])
        .field("aq_level", prediction["aq_level"])
        .field("confidence", prediction["confidence"])
        .field("anomaly_score", prediction["anomaly_score"])
        .field("is_anomaly", int(prediction["is_anomaly"]))
    )

    for k, v in features.items():
        point = point.field(k, float(v))

    write_api.write(bucket=INFLUX_BUCKET, record=point)
