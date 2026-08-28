from fastapi import FastAPI

from backend.app.routes.prediction import router as prediction_router

app = FastAPI(title="Aura: Pearls AQI Predictor")

app.include_router(prediction_router)


@app.get("/")
def root():
    return {"message": "Aura API is running"}