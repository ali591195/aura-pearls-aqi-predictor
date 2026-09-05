from fastapi import APIRouter

from backend.app.schemas.technical_details import (
    TechnicalDetailsResponse,
)
from backend.app.services.technical_details import (
    get_technical_details,
)

router = APIRouter(
    prefix="/api",
    tags=["Technical Details"]
)


@router.get(
    "/technical-details",
    response_model=TechnicalDetailsResponse
)
def technical_details() -> TechnicalDetailsResponse:
    return get_technical_details()