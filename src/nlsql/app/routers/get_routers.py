from fastapi import APIRouter
from typing import List, Callable
from .healthcheck import get_router as healthcheck
from .model import get_router as model


def get_routers() -> List[Callable[[], APIRouter]]:
    return [
        healthcheck,
        model
    ]