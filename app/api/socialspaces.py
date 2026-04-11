from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal

router = APIRouter(prefix="/socialspaces", tags=["SocialSpaces"])


# 🔹 DB Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# 🔥 GET ALL SOCIALSPACES (OPTIONAL - FOR DEBUG / FUTURE)
@router.get("/")
def get_all_socialspaces(db: Session = Depends(get_db)):
    results = db.execute("""
        SELECT id, name, type, parent_id
        FROM socialspaces
        ORDER BY name
    """).fetchall()

    return [
        {
            "id": r[0],
            "name": r[1],
            "type": r[2],
            "parent_id": r[3]
        }
        for r in results
    ]


# 🔥 GET ONLY POLYGON-BASED SOCIALSPACES (FOR DROPDOWN)
@router.get("/polygons")
def get_polygon_socialspaces(db: Session = Depends(get_db)):
    results = db.execute("""
        SELECT id, name
        FROM socialspaces
        WHERE boundary IS NOT NULL
        ORDER BY name
    """).fetchall()

    return [
        {
            "id": r[0],
            "name": r[1]
        }
        for r in results
    ]


# 🔥 GET SINGLE SOCIALSPACE (FOR FUTURE USE)
@router.get("/{socialspace_id}")
def get_socialspace(socialspace_id: int, db: Session = Depends(get_db)):
    result = db.execute("""
        SELECT id, name, type, parent_id
        FROM socialspaces
        WHERE id = :id
    """, {"id": socialspace_id}).fetchone()

    if not result:
        raise HTTPException(status_code=404, detail="Social space not found")

    return {
        "id": result[0],
        "name": result[1],
        "type": result[2],
        "parent_id": result[3]
    }