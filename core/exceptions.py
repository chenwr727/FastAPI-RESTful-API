from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException

from core.logging import logger
from core.response import StandardResponse


class NotFoundError(HTTPException):
    def __init__(self, item_name: str, item_id: int):
        super().__init__(status_code=404, detail=f"{item_name} not found with ID: {item_id}")


async def validation_exception_handler(request: Request, exc: RequestValidationError):
    logger.error(f"Validation error: {exc.errors()}")
    return JSONResponse(
        status_code=422,
        content=StandardResponse(status="error", data={}, message=str(exc.errors())).model_dump(),
    )


async def http_exception_handler(request: Request, exc: HTTPException):
    logger.error(f"HTTP error: {exc.detail}")
    return JSONResponse(
        status_code=exc.status_code,
        content=StandardResponse(status="error", data={}, message=exc.detail).model_dump(),
    )


async def generic_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled exception: {exc}")
    return JSONResponse(
        status_code=500,
        content=StandardResponse(status="error", data={}, message=str(exc)).model_dump(),
    )


def configure_exception_handlers(app: FastAPI):
    app.add_exception_handler(RequestValidationError, validation_exception_handler)
    app.add_exception_handler(HTTPException, http_exception_handler)
    app.add_exception_handler(Exception, generic_exception_handler)
