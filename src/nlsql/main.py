from fastapi import FastAPI, Depends
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from app.core.client import HTTPClient
from typing import Annotated

from app.core.error_handling import mount_error_handling
from app.routers.get_routers import get_routers
from dotenv import load_dotenv

load_dotenv()
app = FastAPI(title='nlsql', description='nlsql model')

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

mount_error_handling(app)

client = Annotated[HTTPClient, Depends(HTTPClient.get_client())]

for router in get_routers():
    app.include_router(router(client))

@app.get("/")
async def root() -> JSONResponse:
    return JSONResponse({"message": "hello world"})

