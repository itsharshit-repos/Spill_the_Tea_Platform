from fastapi import FastAPI, HTTPException, status, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field
from database import engine, get_db
import models

app = FastAPI()

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

@app.post("/spill-tea", response_model=TeaResponse, status_code=201)
def create_tea(tea: TeaCreate, db: Session = Depends(get_db)):
    new_tea = models.Tea(title=tea.title, content=tea.content)
    # add it to the database
    db.add(new_tea)
    # save it permanently to the PostgreSQL disk
    db.commit()
    # refresh it to get the auto-generated ID back from PostgreSQL
    db.refresh(new_tea)
    return new_tea

@app.get("/spill-tea", response_model=list[TeaResponse])
def get_all_tea(db: Session = Depends(get_db)):
    all_teas = db.query(models.Tea).all()
    return all_teas

@app.get("/spill-tea/{tea_id}", response_model=TeaResponse)
def get_tea_by_id(tea_id: int, db: Session = Depends(get_db)):
    tea_item = db.query(models.Tea).filter(models.Tea.id == tea_id).first()

    if tea_item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tea not found")

    return tea_item

@app.patch("/spill-tea/{tea_id}", response_model=TeaResponse)
def update_tea(tea_id: int, tea_update: TeaUpdate, db: Session = Depends(get_db)):
    # fetching existing record from database
    tea_item = db.query(models.Tea).filter(models.Tea.id == tea_id).first()

    # if it doesn't exist, raise 404 error
    if tea_item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tea not found"
        )
    # update only fields provided by the client
    update_data = tea_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(tea_item, key, value)
            
    # commit changes
    db.commit()
    db.refresh(tea_item)
    return tea_item

@app.delete("/spill-tea/{tea_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_tea(tea_id: int, db: Session = Depends(get_db)):
    tea_item = db.query(models.Tea).filter(models.Tea.id == tea_id).first()
    # raise 404 error if tea not found
    if tea_item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tea not found"
        )
    # delete the tea post and commit change
    db.delete(tea_item)
    db.commit()
    return 