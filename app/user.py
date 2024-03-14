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
def create_user(request: schemas.UserBase, db: Session = Depends(get_db)):
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