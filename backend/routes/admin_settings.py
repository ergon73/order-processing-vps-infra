from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from datetime import datetime
from core.database import get_db
from models.admin_settings import AdminSettings, AdminSettingsCRUD

router = APIRouter(prefix="/admin-settings", tags=["Admin Settings"])

class AdminSettingsCreate(BaseModel):
    services: str
    budget_range: str

class AdminSettingsResponse(BaseModel):
    id: int
    services: str
    budget_range: str
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

@router.post("/", response_model=AdminSettingsResponse)
def create_admin_setting(data: AdminSettingsCreate, db: Session = Depends(get_db)):
    result = AdminSettingsCRUD.create(db, services=data.services, budget_range=data.budget_range)
    return result

@router.get("/latest", response_model=AdminSettingsResponse)
def get_latest_settings(db: Session = Depends(get_db)):
    result = AdminSettingsCRUD.get_latest(db)
    if not result:
        return {"id": 0, "services": "", "budget_range": "", "created_at": datetime.now(), "updated_at": datetime.now()}
    return result

@router.get("/", response_model=list[AdminSettingsResponse])
def get_all_settings(db: Session = Depends(get_db)):
    return AdminSettingsCRUD.get_all(db)
