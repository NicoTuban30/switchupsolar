from fastapi import APIRouter, Depends,  HTTPException, status
from app import models
from app import schemas
from sqlalchemy.orm import Session
from app.database import get_db
import uuid

router = APIRouter(
    prefix="/api/users",
    tags=['user']
)

# CREATE A USER
@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(request: schemas.UserBase, db: Session = Depends(get_db)):
    new_user = models.User(
        id = str(uuid.uuid4()),
        first_name = request.first_name,
        last_name = request.last_name,
        phone_number = request.phone_number,
        email = request.email,
        street = request.street,
        city = request.city,
        state = request.state,
        zip_code = request.zip_code,
        electric_bill = request.electric_bill,
        electric_utility = request.electric_utility,
        roof_shade = request.roof_shade  
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"Status": "Success", "User": new_user}

# FETCH ALL USERS AVAILABLE
@router.get("/", status_code=status.HTTP_200_OK)
async def get_all_users(db: Session = Depends(get_db)):
    users = db.query(models.User).all()
    if users is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return {"Count" : len(users), "Users": users }


@router.get("/{user_id}")
async def get_single_user(user_id: str, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with an ID of {user_id} does not exist")
    return user
