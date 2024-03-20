from fastapi_utils.guid_type import GUID, GUID_DEFAULT_SQLITE
from sqlalchemy import TIMESTAMP, CheckConstraint, Column, String
from sqlalchemy.sql import func

from app.database import Base


class AuthUser(Base):
    __tablename__ = "auth_users"
    id = Column(GUID, primary_key=True, default=GUID_DEFAULT_SQLITE)
    username = Column(String, nullable=False)
    password = Column(String, nullable=False)
    createdAt = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=func.now()
    )
    updatedAt = Column(TIMESTAMP(timezone=True), default=None, onupdate=func.now())

    __table_args__ = (
        CheckConstraint("length(username) > 0", name="non_empty_username"),
        CheckConstraint("length(password) > 0", name="non_empty_password"),
    )
