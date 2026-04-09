from fastapi import APIRouter
from app.database import SessionLocal
from app.models.user import User
from app.schemas.user import UserCreate

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/")
def register_user(user: UserCreate):
     
    print("🔥 register_user HIT") 
    db = SessionLocal()

    new_user = User(
        name=user.name,
        date_of_birth=user.date_of_birth,
        gender=user.gender,
        phone_number=user.phone_number,
        latitude=user.latitude,
        longitude=user.longitude
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    db.close()

    return {
        "message": "User created",
        "user_id": new_user.id
    }