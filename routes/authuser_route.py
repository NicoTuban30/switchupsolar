import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.database import get_db
from app.hash import Hash
from models import authuser_model
from schemas import authuser_schema

router = APIRouter(prefix="/api/auth", tags=["authuser"])


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
    except IntegrityError:
        # Catch IntegrityError, which might occur if there's a unique constraint violation
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Fill-up Fields Correctly!"
        )
    except Exception as e:
        # Catch any other unexpected exceptions and provide a generic error message
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))