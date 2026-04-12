from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.database import SessionLocal

router = APIRouter(prefix="/socialspaces", tags=["SocialSpaces"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/")
def get_all_socialspaces(db: Session = Depends(get_db)):
    print("🔥 HIT /socialspaces")

    results = db.execute(text("""
        SELECT id, name, type
        FROM socialspaces
        ORDER BY name
    """)).fetchall()

    return [
        {
            "id": r[0],
            "name": r[1],
            "type": r[2]
        }
        for r in results
    ]