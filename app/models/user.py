from sqlalchemy import Column, Integer, String, Date, Float,DateTime
from app.database import Base
from sqlalchemy.sql import func

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    date_of_birth = Column(Date)
    gender = Column(String)
    phone_number = Column(String)
    latitude = Column(Float)
    longitude = Column(Float)
    created_at = Column(DateTime, server_default=func.now())
    