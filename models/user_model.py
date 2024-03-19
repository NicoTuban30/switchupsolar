from fastapi_utils.guid_type import GUID, GUID_DEFAULT_SQLITE
from sqlalchemy import TIMESTAMP, Column, Integer, String
from sqlalchemy.sql import func

from app.database import Base


class User(Base):
    __tablename__ = "users"
    id = Column(GUID, primary_key=True, default=GUID_DEFAULT_SQLITE)
    first_name = Column(String(20), nullable=False)
    last_name = Column(String(20), nullable=False)
    phone_number = Column(String, nullable=False)
    email = Column(String(100), nullable=False, unique=True)
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
