from fastapi import APIRouter
from ..schema.health import Health

def get_router(client):
    router = APIRouter()

    @router.get("/healthcheck")
    async def healthcheck()-> Health:
        return Health(status=200)

    return router
