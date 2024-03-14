from pydantic import BaseModel
from datetime import datetime

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
