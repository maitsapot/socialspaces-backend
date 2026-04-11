from pydantic import BaseModel, Field
from datetime import date

class UserCreate(BaseModel):
    firebase_uid: str
    name: str = Field(min_length=2)
    date_of_birth: date
    gender: str
    phone_number: str
    latitude: float
    longitude: float
    social_space_id: int 