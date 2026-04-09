# app/models/profile.py

from sqlalchemy import Column, Integer, String, ForeignKey
from app.database import Base


class Profile(Base):
    __tablename__ = "profiles"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True)

    name = Column(String)
    gender = Column(String)