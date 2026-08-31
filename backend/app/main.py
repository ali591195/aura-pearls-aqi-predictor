import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

from backend.app.routes.prediction import router as prediction_router


load_dotenv()

app = FastAPI(title="Aura: Pearls AQI Predictor")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[f"http://{os.getenv("FRONTEND_HOST", "localhost")}localhost:{os.getenv("FRONTEND_PORT", "5173")}"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(prediction_router)


@app.get("/")
def root():
    return {"message": "Aura API is running"}