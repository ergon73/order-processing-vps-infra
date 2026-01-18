from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from datetime import datetime
from core.database import get_db
from models.applications import Application, ApplicationCRUD

router = APIRouter(prefix="/applications", tags=["Applications"])

class ApplicationCreate(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    middle_name: str | None = None
    business_info: str | None = None
    budget: str | None = None
    preferred_contact_method: str | None = None
    comments: str | None = None
    business_niche: str | None = None
    company_size: str | None = None
    task_scope: str | None = None
    user_role: str | None = None
    business_size: str | None = None
    need_volume: str | None = None
    deadline: str | None = None
    task_type: str | None = None
    interested_product: str | None = None
    preferred_contact: str | None = None
    convenient_time: str | None = None

class ApplicationResponse(BaseModel):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

@router.post("/", response_model=ApplicationResponse, status_code=201)
def create_application(data: ApplicationCreate, db: Session = Depends(get_db)):
    result = ApplicationCRUD.create(db, **data.model_dump())
    return result

@router.get("/", response_model=list[ApplicationResponse])
def get_all_applications(db: Session = Depends(get_db)):
    return ApplicationCRUD.get_all(db)
