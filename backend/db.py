import time
import os
from dotenv import load_dotenv                                                                                         #type:ignore                                                     
from influxdb_client import InfluxDBClient, Point                                                                      #type:ignore
from influxdb_client.client.write_api import SYNCHRONOUS                                                               #type:ignore
load_dotenv()

INFLUX_URL = os.getenv("INFLUX_URL")
INFLUX_TOKEN = os.getenv("INFLUX_TOKEN")
ORG = os.getenv("INFLUX_ORG")
BUCKET = os.getenv("INFLUX_BUCKET")

#DB
client = InfluxDBClient(url=INFLUX_URL,token=INFLUX_TOKEN,org=ORG)

write_api = client.write_api(write_options=SYNCHRONOUS)

#write
def write_to_influx(
    temp,
    hum,
    mq,
    feats,
    aq_level,
    confidence,
    anomaly,
    anomaly_score
):
    ts = int(time.time() * 1e9)

    point = (
        Point("air_quality")
        .time(ts)
        .field("temp", float(temp))
        .field("hum", float(hum))
        .field("mq", float(mq))
        .field("aq_level", int(aq_level))
        .field("confidence", float(confidence))
        .field("is_anomaly", int(anomaly))
        .field("anomaly_score", float(anomaly_score))
    )

    for k, v in feats.items():
        point = point.field(k, float(v))

    write_api.write(bucket=BUCKET, record=point)
