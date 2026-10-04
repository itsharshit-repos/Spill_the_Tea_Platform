from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field

app = FastAPI()

fake_db = []

class TeaCreate(BaseModel):
    title: str = Field(..., min_length=3, max_length=50)
    content: str = Field(..., min_length=10, max_length=1000)

class TeaResponse(BaseModel):
    id: int 
    title: str
    content: str

@app.post("/spill-tea", response_model=TeaResponse, status_code=201)
def create_tea(tea: TeaCreate):
    new_id = len(fake_db) + 1
    new_tea = {
        "id": new_id,
        "title": tea.title,
        "content": tea.content
    }
    fake_db.append(new_tea)
    return new_tea

@app.get("/spill-tea", response_model=list[TeaResponse])
def get_all_tea():
    return fake_db

@app.get("/spill-tea/{tea_id}", response_model=TeaResponse)
def get_tea_by_id(tea_id: int):
    for tea_item in fake_db:
        if tea_item.get("id") == tea_id:
            return tea_item
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Tea not found"
    )