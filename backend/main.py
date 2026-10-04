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

class TeaUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=3, max_length=50)
    content: str | None = Field(default=None, min_length=10, max_length=1000)

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

@app.patch("/spill-tea/{tea_id}", response_model=TeaResponse)
def update_tea(tea_id: int, tea_update: TeaUpdate):
    for tea_item in fake_db:
        if tea_item.get("id") == tea_id:
            # when tea id is matched then we move to update the tea title or content or both
            if tea_update.title is not None:
                tea_item["title"] = tea_update.title
            if tea_update.content is not None:
                tea_item["content"] = tea_update.content
            # returning tea after update
            return tea_item
    # Raising error if tea not found
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Tea not found"
    )

@app.delete("/spill-tea/{tea_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_tea(tea_id: int):
    for index, tea_item in enumerate(fake_db):
        if tea_item["id"] == tea_id:
            fake_db.pop(index)
            return # return nothing. FastAPI automatically return the clean 204 response
    # raising exception if tea not found
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Tea not found"
    )