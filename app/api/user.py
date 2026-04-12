from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.user import User
from app.models.profile import Profile
from app.schemas.user import UserCreate
from geoalchemy2.shape import from_shape
from shapely.geometry import Point

# 🔥 Router setup
router = APIRouter(prefix="/users", tags=["Users"])


# 🔹 Database session dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# 🔥 UPSERT USER (Create or Update)
@router.post("/")
def upsert_user(user: UserCreate, db: Session = Depends(get_db)):

    print("🔥 /users HIT")

    # 🔹 BASIC VALIDATION
    if user.latitude is None or user.longitude is None:
        raise HTTPException(status_code=400, detail="Location required")

    if user.social_space_id is None:
        raise HTTPException(status_code=400, detail="Social space required")

    # 🔹 Check if user exists (by firebase UID)
    existing_user = db.query(User).filter_by(
        firebase_uid=user.firebase_uid
    ).first()

    is_new_user = False

    # 🔥 CREATE USER if not exists
    if not existing_user:
        print("🆕 Creating new user")

        existing_user = User(
            firebase_uid=user.firebase_uid
        )

        db.add(existing_user)
        db.commit()
        db.refresh(existing_user)

        is_new_user = True

    # 🔥 Ensure PROFILE exists for this user
    profile = db.query(Profile).filter_by(user_id=existing_user.id).first()

    if not profile:
        profile = Profile(user_id=existing_user.id)

        db.add(profile)
        db.commit()
        db.refresh(profile)

    # 🔥 Build GEO POINT (longitude, latitude)
    try:
        point = Point(user.longitude, user.latitude)
        existing_user.location = from_shape(point, srid=4326)
    except Exception as e:
        print("❌ LOCATION ERROR:", e)
        raise HTTPException(status_code=400, detail="Invalid location")

    # 🔥 UPDATE USER CORE FIELDS
    existing_user.phone_number = user.phone_number
    existing_user.social_space_id = user.social_space_id

    # 🔥 Mark profile as complete (currently forced true)
    existing_user.is_profile_complete = True

    # 🔥 UPDATE PROFILE FIELDS
    profile.name = user.name
    profile.gender = user.gender.lower()
    profile.date_of_birth = user.date_of_birth

    # 🔥 Commit ALL changes (User + Profile)
    db.commit()

    # 🔥 Refresh user instance
    db.refresh(existing_user)

    # 🔥 RESPONSE
    return {
        "message": "User saved",
        "user_id": existing_user.id,
        "is_new_user": is_new_user,
        "is_profile_complete": existing_user.is_profile_complete
    }