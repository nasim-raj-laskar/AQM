from fastapi import FastAPI
from app.api.routes import router

app = FastAPI(title="Modular Air Quality ML Backend")
app.include_router(router)
