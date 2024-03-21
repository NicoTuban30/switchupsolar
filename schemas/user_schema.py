from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, EmailStr


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


# to contain no createdAt field
class UserBaseUpdate(BaseModel):
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
    updatedAt: datetime | None = None


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
