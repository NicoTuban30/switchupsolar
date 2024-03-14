from app.database import Base
from sqlalchemy import TIMESTAMP, Column, String, Boolean, Integer
from fastapi_utils.guid_type import GUID, GUID_DEFAULT_SQLITE
from sqlalchemy.orm import validates
import re
from sqlalchemy.sql import func

class User(Base):
    __tablename__ = "users"
    id = Column(GUID, primary_key=True, default=GUID_DEFAULT_SQLITE)
    first_name = Column(String)
    last_name = Column(String)
    phone_number = Column(String)
    email = Column(String)
    street = Column(String)
    city = Column(String)
    state = Column(String)
    zip_code = Column(String)
    electric_bill = Column(Integer)
    electric_utility = Column(Integer)
    roof_shade = Column(String)
    createdAt = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=func.now()
    )
    updatedAt = Column(TIMESTAMP(timezone=True), default=None, onupdate=func.now())

    @validates('email')
    def validate_email(self, key, email):
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            raise ValueError("Invalid email format")
        return email
