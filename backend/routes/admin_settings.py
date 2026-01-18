from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel
from datetime import datetime
from core.database import get_db
from models.admin_settings import AdminSettings, AdminSettingsCRUD
from routes.auth import get_current_admin

router = APIRouter(prefix="/admin-settings", tags=["Admin Settings"])

class AdminSettingsCreate(BaseModel):
    services: str
    budget_range: str

class AdminSettingsUpdate(BaseModel):
    services: str | None = None
    budget_range: str | None = None

class AdminSettingsResponse(BaseModel):
    id: int
    services: str
    budget_range: str
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

@router.post("/", response_model=AdminSettingsResponse, status_code=status.HTTP_201_CREATED)
def create_admin_setting(
    data: AdminSettingsCreate,
    db: Session = Depends(get_db),
    current_admin = Depends(get_current_admin)  # Требует JWT
):
    """Создать новую услугу (требует JWT авторизацию)"""
    result = AdminSettingsCRUD.create(db, services=data.services, budget_range=data.budget_range)
    return result

@router.put("/{id}", response_model=AdminSettingsResponse)
def update_admin_setting(
    id: int,
    data: AdminSettingsUpdate,
    db: Session = Depends(get_db),
    current_admin = Depends(get_current_admin)  # Требует JWT
):
    """Обновить услугу (требует JWT авторизацию)"""
    admin_setting = db.query(AdminSettings).filter(AdminSettings.id == id).first()
    if not admin_setting:
        raise HTTPException(status_code=404, detail="Service not found")
    
    if data.services is not None:
        admin_setting.services = data.services
    if data.budget_range is not None:
        admin_setting.budget_range = data.budget_range
    
    db.commit()
    db.refresh(admin_setting)
    return admin_setting

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_admin_setting(
    id: int,
    db: Session = Depends(get_db),
    current_admin = Depends(get_current_admin)  # Требует JWT
):
    """Удалить услугу (требует JWT авторизацию)"""
    admin_setting = db.query(AdminSettings).filter(AdminSettings.id == id).first()
    if not admin_setting:
        raise HTTPException(status_code=404, detail="Service not found")
    
    db.delete(admin_setting)
    db.commit()
    return None

@router.get("/latest", response_model=AdminSettingsResponse)
def get_latest_settings(db: Session = Depends(get_db)):
    """Получить последнюю услугу (публичный)"""
    result = AdminSettingsCRUD.get_latest(db)
    if not result:
        return {"id": 0, "services": "", "budget_range": "", "created_at": datetime.now(), "updated_at": datetime.now()}
    return result

@router.get("/", response_model=list[AdminSettingsResponse])
def get_all_settings(db: Session = Depends(get_db)):
    """Получить все услуги (публичный)"""
    return AdminSettingsCRUD.get_all(db)
