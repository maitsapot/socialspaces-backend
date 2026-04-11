from sqlalchemy import Column, Integer, String, Date, Float, DateTime, Boolean
from geoalchemy2 import Geometry
from sqlalchemy.sql import func
from app.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)

    firebase_uid = Column(String, unique=True, index=True, nullable=False)

    name = Column(String, nullable=True)
    date_of_birth = Column(Date, nullable=True)
    gender = Column(String(10), nullable=True)

    phone_number = Column(String, index=True)

        
    location =Column(Geometry('POINT',srid=4326))

    is_profile_complete = Column(Boolean, default=False)

    created_at = Column(DateTime, server_default=func.now())