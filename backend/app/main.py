import os

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.app.routes.prediction import (
    router as prediction_router,
)
from backend.app.routes.current_air_quality import (
    router as current_air_quality_router,
)
from backend.app.routes.current_weather import (
    router as current_weather_router,
)


load_dotenv()

app = FastAPI(title="Aura: Pearls AQI Predictor")

frontend_host = os.getenv("FRONTEND_HOST", "localhost")
frontend_port = os.getenv("FRONTEND_PORT")

frontend_url = (
    f"http://{frontend_host}:{frontend_port}"
    if frontend_port
    else f"https://{frontend_host}"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[frontend_url],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(prediction_router)
app.include_router(current_air_quality_router)
app.include_router(current_weather_router)


@app.get("/")
def root():
    return {"message": "Aura API is running"}