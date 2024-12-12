from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import engine
from .models import user, Campaign as campaign_model
from .routers import auth, campaigns

# Create database tables
user.Base.metadata.create_all(bind=engine)
campaign_model.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Campaign Management API")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, tags=["Authentication"])
app.include_router(campaigns.router, prefix="/campaigns", tags=["Campaigns"])

@app.get("/")
async def root():
    return {"message": "Welcome to the Campaign Management API"}