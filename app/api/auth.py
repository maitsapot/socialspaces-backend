# app/api/auth.py

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from app.schemas.auth import LoginRequest
from app.database import SessionLocal
from app.models.user import User
from app.models.profiles import Profile

from firebase_admin import auth as firebase_auth

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
        decoded_token = firebase_auth.verify_id_token(request.token)
        firebase_uid = decoded_token["uid"]
        phone_number = decoded_token.get("phone_number")

    except Exception:
        raise HTTPException(status_code=401, detail="Invalid Firebase token")

    # 🔍 Check if user exists
    user = db.query(User).filter_by(firebase_uid=firebase_uid).first()

    if not user:
        user = User(
            firebase_uid=firebase_uid,
            phone_number=phone_number
        )
        db.add(user)
        db.commit()
        db.refresh(user)

        # Create empty profile
        profile = Profile(user_id=user.id)
        db.add(profile)
        db.commit()
    else:
        profile = db.query(Profile).filter_by(user_id=user.id).first()

    return {
        "user_id": user.id,
        "firebase_uid": firebase_uid,
        "profile": {
            "name": profile.name if profile else None,
            "gender": profile.gender if profile else None
        },
        "is_new_user": profile.name is None
    }