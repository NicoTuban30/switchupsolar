import uuid
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from auth.oauth2 import get_current_user
from models import user_model
from schemas import authuser_schema, user_schema

router = APIRouter(prefix="/api/users", tags=["user"])


# CREATE A USER
@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(
    request: user_schema.UserBase,
    db: Session = Depends(get_db),
    current_user: authuser_schema = Depends(get_current_user),
):

    try:
        new_user = user_model.User(
            id=str(uuid.uuid4()),
            first_name=request.first_name,
            last_name=request.last_name,
            phone_number=request.phone_number,
            email=request.email,
            street=request.street,
            city=request.city,
            state=request.state,
            zip_code=request.zip_code,
            electric_bill=request.electric_bill,
            electric_utility=request.electric_utility,
            roof_shade=request.roof_shade,
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return {"Status": "Success", "User": new_user}
    except Exception:
        # Catch IntegrityError, which might occur if there's a unique constraint violation
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="An error occurred while creating the user!",
        )


# FETCH ALL USERS AVAILABLE
@router.get(
    "/", status_code=status.HTTP_200_OK, response_model=List[user_schema.UserDisplay]
)
async def get_all_users(
    db: Session = Depends(get_db),
    current_user: authuser_schema = Depends(get_current_user),
):
    users = db.query(user_model.User).all()
    if users is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return users


# FETCH A SINGLE USER
@router.get("/{user_id}", response_model=user_schema.UserDisplay)
async def get_single_user(
    user_id: str,
    db: Session = Depends(get_db),
    current_user: authuser_schema = Depends(get_current_user),
):
    try:
        user = db.query(user_model.User).filter(user_model.User.id == user_id).first()
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with an ID of {user_id} does not exist",
            )
        return user
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with an ID of {user_id} does not exist",
        )


# UPDATE A SINGLE USER
@router.put("/{user_id}", status_code=status.HTTP_202_ACCEPTED)
async def update_user(
    user_id: str,
    request: user_schema.UserBaseUpdate,
    db: Session = Depends(get_db),
    current_user: authuser_schema = Depends(get_current_user),
):
    try:
        user_query = db.query(user_model.User).filter(user_model.User.id == user_id)
        user = user_query.first()
        update_data = request.dict(exclude_unset=True)
        user_query.filter(user_model.User.id == user_id).update(
            update_data, synchronize_session=False
        )
        db.commit()
        db.refresh(user)
        return {"Status": "Success", "User": user}
    except Exception:
        # Catch IntegrityError, which might occur if there's a unique constraint violation
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="An error occurred while updating the user!",
        )


# DELETE A SINGLE USER
@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: str,
    db: Session = Depends(get_db),
    current_user: authuser_schema = Depends(get_current_user),
):
    try:
        user_query = db.query(user_model.User).filter(user_model.User.id == user_id)
        user = user_query.first()
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with an ID of {user_id} does not exist!",
            )
        user_query.delete(synchronize_session=False)
        db.commit()
        return {"Status": "Success", "Message": "User deleted successfully!"}
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with an ID of {user_id} does not exist!",
        )
