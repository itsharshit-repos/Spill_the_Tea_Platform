from pydantic import BaseModel, Field

class TeaCreate(BaseModel):
    title: str = Field(..., min_length=3, max_length=50)
    content: str = Field(..., min_length=10, max_length=1000)

class TeaResponse(BaseModel):
    id: int 
    title: str
    content: str
    
    model_config = {"from_attributes": True}

class TeaUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=3, max_length=50)
    content: str | None = Field(default=None, min_length=10, max_length=1000)