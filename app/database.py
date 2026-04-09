# app/db/session.py

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,declarative_base

DATABASE_URL = "postgresql://eyetea:Lerato123@socialspaces-db.postgres.database.azure.com:5432/socialspaces?sslmode=require"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()