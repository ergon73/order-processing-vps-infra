from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from core.database import engine, Base
from routes import admin_settings, applications

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Autéllo Backend API",
    description="Backend for order processing",
    version="1.0.0",
    root_path="/api"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(admin_settings.router)
app.include_router(applications.router)

@app.get("/")
def root():
    return {"message": "Autéllo Backend API is running"}
