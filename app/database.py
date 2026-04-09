# app/db/session.py

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "postgresql://eyetea:Lerato123@socialspaces-odoo-db.postgres.database.azure.com:5432/socialspaces?sslmode=require"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)