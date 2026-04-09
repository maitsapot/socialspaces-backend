# app/api/profile.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models.user import User
from app.models.profile import Profile

router = APIRouter(prefix="/profile", tags=["Profile"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/update")
def update_profile(payload: dict, db: Session = Depends(get_db)):
    firebase_uid = payload.get("firebase_uid")

    if not firebase_uid:
        raise HTTPException(status_code=400, detail="Missing firebase_uid")

    user = db.query(User).filter_by(firebase_uid=firebase_uid).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # 🔍 Get or create profile
    profile = db.query(Profile).filter_by(user_id=user.id).first()

    if not profile:
        profile = Profile(user_id=user.id)
        db.add(profile)

    # 🔥 Update profile fields
    profile.name = payload.get("name")
    profile.gender = payload.get("gender")

    db.commit()

    return {
        "message": "Profile updated",
        "user_id": user.id
    }