from fastapi import APIRouter, Header, HTTPException
from app.firebase import verify_firebase_token
from app.database import SessionLocal
from app.models.user import User

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/login")
def login(authorization: str = Header(...)):
    token = authorization.split("Bearer ")[-1]

    decoded = verify_firebase_token(token)

    if not decoded:
        raise HTTPException(status_code=401, detail="Invalid token")

    firebase_uid = decoded["uid"]

    db = SessionLocal()

    user = db.query(User).filter(User.firebase_uid == firebase_uid).first()

    if not user:
        user = User(firebase_uid=firebase_uid)
        db.add(user)
        db.commit()
        db.refresh(user)

    db.close()

    return {
        "message": "Authenticated",
        "user_id": user.id
    }