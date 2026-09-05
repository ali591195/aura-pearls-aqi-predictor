import os
import sys
import ctypes
from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

if sys.platform.startswith("linux"):
    libgomp_path = Path(__file__).resolve().parents[2] / "lib/libgomp.so.1"

    print(f"libgomp path: {libgomp_path}")
    print(f"libgomp exists: {libgomp_path.exists()}")

    ctypes.CDLL(
        str(libgomp_path),
        mode=ctypes.RTLD_GLOBAL,
    )

from backend.app.routes.prediction import router as prediction_router
from backend.app.routes.current_air_quality import router as current_air_quality_router
from backend.app.routes.current_weather import router as current_weather_router
from backend.app.routes.raw_historical_backfill import router as raw_historical_backfill_router
from backend.app.routes.engineered_historical_backfill import router as engineered_historical_backfill_router
from backend.app.routes.model_training import router as model_training_router
from backend.app.routes.technical_details import router as technical_details_router


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
app.include_router(raw_historical_backfill_router)
app.include_router(engineered_historical_backfill_router)
app.include_router(model_training_router)
app.include_router(technical_details_router)


@app.get("/")
def root():
    return {"message": "Aura API is running"}