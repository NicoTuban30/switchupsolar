import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.hash import Hash
from models import authuser_model
from schemas import authuser_schema

router = APIRouter(prefix="/api/auth", tags=["authuser"])


# Enpoint for registration of user to be used as a valid user for authentication later on
@router.post("/", status_code=status.HTTP_201_CREATED)
async def register_user(
    request: authuser_schema.AuthSchema, db: Session = Depends(get_db)
):
    try:
        new_authenticated_user = authuser_model.AuthUser(
            id=str(uuid.uuid4()),
            username=request.username,
            password=Hash.bcrypt(request.password),
        )
        db.add(new_authenticated_user)
        db.commit()
        db.refresh(new_authenticated_user)
        return {"Registration Complete", new_authenticated_user}
    except Exception:
        # Catch IntegrityError, which might occur if there's a unique constraint violation
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="An error occurred while creating the user!",
        )


# obtaining a user with that username to be used in the authentication
def get_user_by_username(username: str, db: Session = Depends(get_db)):
    user = (
        db.query(authuser_model.AuthUser)
        .filter(authuser_model.AuthUser.username == username)
        .first()
    )
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with username {username} not found",
        )
    return user
