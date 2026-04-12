# app/api/auth.py

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from app.schemas.auth import LoginRequest
from app.database import SessionLocal
from app.models.user import User
from app.models.profile import Profile

from app.firebase import verify_firebase_token

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/auth/login")
def login(request: LoginRequest, db: Session = Depends(get_db)):
    try:
        decoded_token = verify_firebase_token(request.token)

        if not decoded_token:
            raise HTTPException(status_code=401, detail="Invalid Firebase token")

        firebase_uid = decoded_token["uid"]
        phone_number = decoded_token.get("phone_number")

    except Exception:
        raise HTTPException(status_code=401, detail="Invalid Firebase token")

    # 🔍 Check if user exists
    user = db.query(User).filter_by(firebase_uid=firebase_uid).first()

    if not user:
        # 🔥 CREATE USER
        user = User(
            firebase_uid=firebase_uid,
            phone_number=phone_number
        )
        db.add(user)
        db.commit()
        db.refresh(user)

        # 🔥 CREATE EMPTY PROFILE
        profile = Profile(user_id=user.id)
        db.add(profile)
        db.commit()
        db.refresh(profile)

    else:
        # 🔍 FETCH PROFILE
        profile = db.query(Profile).filter_by(user_id=user.id).first()

        # 🔥 SAFETY: ensure profile exists
        if not profile:
            profile = Profile(user_id=user.id)
            db.add(profile)
            db.commit()
            db.refresh(profile)

    # 🔥 DETERMINE PROFILE COMPLETION
    is_profile_complete = (
        profile.name is not None and
        profile.gender is not None
    )

    # 🔥 NEW USER LOGIC (UPDATED)
    is_new_user = not is_profile_complete

    return {
        "user_id": user.id,
        "firebase_uid": firebase_uid,
        "profile": {
            "name": profile.name,
            "gender": profile.gender
        },
        "is_new_user": is_new_user,
        "is_profile_complete": is_profile_complete
    }