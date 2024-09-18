from sqlalchemy import Boolean, Column, Integer, String

from app.db.db import Base


class AdminUser(Base):
    __tablename__ = "admin_users"

    id = Column(Integer, primary_key=True)
    username = Column(String(255), unique=True, index=True)
    email = Column(String(255), unique=True, index=True)
    disabled = Column(Boolean, default=False)
    hashed_password = Column(String(255))
