from fastapi_utils.guid_type import GUID, GUID_DEFAULT_SQLITE
from sqlalchemy import TIMESTAMP, CheckConstraint, Column, Integer, String
from sqlalchemy.sql import func

from app.database import Base


class User(Base):
    __tablename__ = "users"
    id = Column(GUID, primary_key=True, default=GUID_DEFAULT_SQLITE, unique=True)
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

    __table_args__ = (
        CheckConstraint("length(first_name) > 0", name="non_empty_first_name"),
        CheckConstraint("length(last_name) > 0", name="non_empty_last_name"),
        CheckConstraint("length(phone_number) > 0", name="non_empty_phone_number"),
        CheckConstraint("length(email) >= 0", name="non_empty_email"),
        CheckConstraint("electric_bill >= 0", name="non_empty_electric_bill"),
        CheckConstraint("electric_utility >= 0", name="non_empty_electric_utility"),
    )
