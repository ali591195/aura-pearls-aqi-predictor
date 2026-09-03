from fastapi import HTTPException


def raise_internal_server_error(error: RuntimeError) -> None:
    raise HTTPException(
        status_code=500,
        detail=str(error),
    ) from error

def raise_bad_gateway_error(error: RuntimeError) -> None:
    raise HTTPException(
        status_code=502,
        detail=str(error),
    ) from error