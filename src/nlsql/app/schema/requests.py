from typing import Optional
from pydantic import BaseModel, Field

class SingleRequestModel(BaseModel):
    input: str = Field(..., alias="input")