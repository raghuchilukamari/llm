from .logger import get_logger
from .exceptions import ApplicationException, NotImplementedException
from fastapi import Request
from fastapi.responses import JSONResponse

logger = get_logger(__name__)

def mount_error_handling(app):

    @app.exception_handler(ApplicationException)
    async def uvicorn_exception_handler(request: Request, exc: ApplicationException):
        error_message = f"server error: {exc.message}"
        logger.error(error_message)
        return JSONResponse(
            status_code=500,
            content={"message": error_message},
        )

    @app.exception_handler(NotImplementedException)
    async def uvicorn_exception_handler(request: Request, exc: NotImplementedException):
        error_message = f"server error:: {exc.message}"
        logger.error(error_message)
        return JSONResponse(
            status_code=501,
            content={"message": error_message},
        )

    @app.exception_handler(NotImplementedError)
    async def uvicorn_exception_handler(request: Request, exc: NotImplementedError):
        error_message = f"server error: {exc.__class__.__name__}"
        logger.error(error_message)
        return JSONResponse(
            status_code=501,
            content={"message": error_message},
        )

    @app.exception_handler(FileNotFoundError)
    async def uvicorn_exception_handler(request: Request, exc: FileNotFoundError):
        error_message = f"server error: {exc.__class__.__name__}"
        logger.error(error_message)
        return JSONResponse(
            status_code=400,
            content={"message": error_message},
        )

    @app.exception_handler(ValueError)
    async def uvicorn_exception_handler(request: Request, exc: ValueError):
        error_message = f"server error: {exc.__class__.__name__}"
        logger.error(error_message)
        return JSONResponse(
            status_code=400,
            content={"message": exc.__str__(),},
        )

