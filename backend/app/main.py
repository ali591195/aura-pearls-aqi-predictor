import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

from backend.app.routes.prediction import router as prediction_router


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


@app.get("/")
def root():
    return {"message": "Aura API is running"}