from fastapi import FastAPI
from app.database import engine, Base

from fastapi.middleware.cors import CORSMiddleware

# Import models so tables are created
from app.models import user

from app.routes.auth import router as auth_router



# Import routes
from app.routes.user import router as user_router

app = FastAPI(title="SocialSpace API")




app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create database tables
Base.metadata.create_all(bind=engine)

# Register routes
app.include_router(user_router)
app.include_router(auth_router)


@app.get("/")
def root():
    return {"status": "SocialSpace API running 🚀"}