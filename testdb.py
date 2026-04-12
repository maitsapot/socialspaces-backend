from app.database import SessionLocal
from sqlalchemy import text

db = SessionLocal()

try:
    result = db.execute(text("SELECT id, name FROM socialspaces")).fetchall()
    print("✅ DB WORKING:", result)
except Exception as e:
    print("❌ DB ERROR:", e)

db.close()