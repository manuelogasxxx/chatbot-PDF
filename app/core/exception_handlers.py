from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError, OperationalError
from starlette.status import HTTP_500_INTERNAL_SERVER_ERROR
import logging

logger = logging.getLogger(__name__)


# 🔴 Error de integridad (FK, UNIQUE, CHECK, etc.)
async def integrity_error_handler(request: Request, exc: IntegrityError):
    return JSONResponse(
        status_code=400,
        content={
            "error": "DATABASE_INTEGRITY_ERROR",
            "detail": "Los datos enviados violan una restricción de la base de datos"
        }
    )


# 🔴 Error de conexión / BD caída
async def operational_error_handler(request: Request, exc: OperationalError):
    return JSONResponse(
        status_code=503,
        content={
            "error": "DATABASE_UNAVAILABLE",
            "detail": "No se pudo conectar con la base de datos"
        }
    )


# 🔴 Error genérico no controlado
async def unhandled_exception_handler(request: Request, exc: Exception):
    logger.exception(exc)  # log completo, NO al cliente

    return JSONResponse(
        status_code=HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": "INTERNAL_SERVER_ERROR",
            "detail": "Ocurrió un error inesperado"
        }
    )
