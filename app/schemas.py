from pydantic import BaseModel
from datetime import datetime
from uuid import uuid4
from typing import Optional

class UserBase(BaseModel):
    id: str | None = None
    first_name: str
    last_name: str 
    phone_number: str
    email: str
    street: str
    city: str
    state: str
    zip_code: str
    electric_bill: int
    electric_utility: int
    roof_shade: str
    createdAt: datetime | None = None
    updatedAt: datetime | None = None


class UserDisplay(BaseModel):
    email: str
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

    class Config():
        orm_mode = True


