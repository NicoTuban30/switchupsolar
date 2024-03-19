import re
from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, EmailStr, validator


class UserBase(BaseModel):
    first_name: str
    last_name: str
    phone_number: str
    email: EmailStr
    street: str
    city: str
    state: str
    zip_code: str
    electric_bill: int
    electric_utility: int
    roof_shade: str
    createdAt: datetime | None = None
    updatedAt: datetime | None = None

    @validator("email")
    def validate_email(cls, v):
        if not re.match(r"^.+@.+\..+$", v):
            raise ValueError("Invalid email address format")
        if not v.endswith(".com"):
            raise ValueError("Email must end with .com")
        return v


class UserDisplay(BaseModel):
    id: UUID
    email: EmailStr
    first_name: str
    last_name: str
    phone_number: str
    state: str
    city: str
    zip_code: str
    street: str
    roof_shade: str
    electric_bill: int
    electric_utility: int
    createdAt: datetime
    updatedAt: datetime | None = None

    class Config:
        orm_mode = True
