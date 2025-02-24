from pydantic import BaseModel, Field

class Health(BaseModel):
    status:int = Field(200, description="Health status")