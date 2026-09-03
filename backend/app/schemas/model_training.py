from pydantic import BaseModel


class ModelTrainingResponse(BaseModel):
    message: str