from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session
from database import get_db
import models
import schemas
import oauth2

router = APIRouter(
    prefix="/spill-tea",
    tags=["Tea"]  # This automatically group these routes in swagger UI
)

@router.post("/", response_model=schemas.TeaResponse, status_code=201)
def create_tea(tea: schemas.TeaCreate, db: Session = Depends(get_db), current_user: models.User = Depends(oauth2.get_current_user)):
    # checking who is currently making this request
    print(f"User {current_user.username} is spilling the tea!")
    
    new_tea = models.Tea(title=tea.title, content=tea.content)
    # add it to the database
    db.add(new_tea)
    # save it permanently to the PostgreSQL disk
    db.commit()
    # refresh it to get the auto-generated ID back from PostgreSQL
    db.refresh(new_tea)
    return new_tea

@router.get("/", response_model=list[schemas.TeaResponse])
def get_all_tea(db: Session = Depends(get_db)):
    all_teas = db.query(models.Tea).all()
    return all_teas

@router.get("/{tea_id}", response_model=schemas.TeaResponse)
def get_tea_by_id(tea_id: int, db: Session = Depends(get_db)):
    tea_item = db.query(models.Tea).filter(models.Tea.id == tea_id).first()
    if tea_item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tea not found")
    return tea_item

@router.patch("/{tea_id}", response_model=schemas.TeaResponse)
def update_tea(tea_id: int, tea_update: schemas.TeaUpdate, db: Session = Depends(get_db)):
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

@router.delete("/{tea_id}", status_code=status.HTTP_204_NO_CONTENT)
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