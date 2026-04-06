from pydantic import BaseModel
from datetime import date

class UserCreate(BaseModel):
    name: str
    date_of_birth: date
    gender: str
    phone_number: str
    latitude: float 
    longitude: float