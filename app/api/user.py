from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.user import User
from app.schemas.user import UserCreate
from geoalchemy2.shape import from_shape
from shapely.geometry import Point

router = APIRouter(prefix="/users", tags=["Users"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/")
def register_user(user: UserCreate, db: Session = Depends(get_db)):

    existing_user = db.query(User).filter_by(
        firebase_uid=user.firebase_uid
    ).first()

    if not existing_user:
        raise HTTPException(status_code=404, detail="User not found")

    # 🔥 CREATE POINT FROM FLUTTER DATA
    point = Point(user.longitude, user.latitude)

    # 🔥 UPDATE USER
    existing_user.name = user.name
    existing_user.date_of_birth = user.date_of_birth
    existing_user.gender = user.gender.lower()
    existing_user.phone_number = user.phone_number
    existing_user.location = from_shape(point, srid=4326)
    existing_user.social_space_id = user.social_space_id
    existing_user.is_profile_complete = True

    db.commit()
    db.refresh(existing_user)

    return {
        "message": "User updated",
        "user_id": existing_user.id
    }