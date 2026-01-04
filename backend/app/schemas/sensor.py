from pydantic import BaseModel

class SensorInput(BaseModel):
    temp: float
    hum: float
    mq: float
