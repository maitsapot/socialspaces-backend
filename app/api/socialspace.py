from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.database import SessionLocal
import logging

router = APIRouter(prefix="/socialspaces", tags=["SocialSpaces"])

logger = logging.getLogger(__name__)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# 🔹 EXISTING
@router.get("/")
def get_all_socialspaces(db: Session = Depends(get_db)):
    logger.info("GET /socialspaces called")

    results = db.execute(text("""
        SELECT id, name, type
        FROM socialspaces
        ORDER BY name
    """)).fetchall()

    return [
        {"id": r[0], "name": r[1], "type": r[2]}
        for r in results
    ]


# 🔥 ENHANCED NEARBY (STRICT + PARENT + CHILD)
@router.get("/nearby")
def get_nearby_socialspaces(
    lat: float = Query(...),
    lon: float = Query(...),
    db: Session = Depends(get_db)
):
    logger.info(f"GET /socialspaces/nearby lat={lat}, lon={lon}")

    # 🔹 STEP 1: STRICT POLYGON MATCH
    results = db.execute(text("""
        SELECT id, name, type, parent_id
        FROM socialspaces
        WHERE boundary IS NOT NULL
          AND ST_Contains(
                boundary,
                ST_SetSRID(ST_MakePoint(:lon, :lat), 4326)
          )
        ORDER BY ST_Area(boundary) ASC
    """), {
        "lat": lat,
        "lon": lon
    }).fetchall()

    spaces = [
        {"id": r[0], "name": r[1], "type": r[2]}
        for r in results
    ]

    if not results:
        return spaces  # empty list (no fallback as per your rule)

    # 🔹 STEP 2: PRIMARY (smallest polygon)
    primary = results[0]
    primary_id = primary[0]
    parent_id = primary[3]

    # 🔹 STEP 3: GET ONE PARENT (if exists and is polygon)
    parent = None
    if parent_id:
        parent_row = db.execute(text("""
            SELECT id, name, type
            FROM socialspaces
            WHERE id = :id
              AND boundary IS NOT NULL
        """), {"id": parent_id}).fetchone()

        if parent_row:
            parent = {
                "id": parent_row[0],
                "name": parent_row[1],
                "type": parent_row[2]
            }

    # 🔹 STEP 4: GET ONE CHILD (nearest child polygon)
    child_row = db.execute(text("""
        SELECT id, name, type
        FROM socialspaces
        WHERE parent_id = :id
          AND boundary IS NOT NULL
        ORDER BY ST_Area(boundary) ASC
        LIMIT 1
    """), {"id": primary_id}).fetchone()

    child = None
    if child_row:
        child = {
            "id": child_row[0],
            "name": child_row[1],
            "type": child_row[2]
        }

    # 🔹 STEP 5: MERGE (NO DUPLICATES)
    final = spaces.copy()

    if parent and parent not in final:
        final.append(parent)

    if child and child not in final:
        final.append(child)

    return final