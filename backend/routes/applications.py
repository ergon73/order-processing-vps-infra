from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel
from datetime import datetime
from core.database import get_db
from models.applications import Application, ApplicationCRUD
from core.priority import calculate_priority_score
from routes.auth import get_current_admin

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
    first_name: str | None
    last_name: str | None
    middle_name: str | None
    business_info: str | None
    budget: str | None
    company_size: str | None
    deadline: str | None
    comments: str | None
    interested_product: str | None
    priority_score: int | None = 0
    created_at: datetime
    
    class Config:
        from_attributes = True

@router.post("/", response_model=ApplicationResponse, status_code=201)
def create_application(data: ApplicationCreate, db: Session = Depends(get_db)):
    # Вычисляем priority_score при создании
    application_dict = data.model_dump()
    application_dict['priority_score'] = calculate_priority_score(data)
    
    result = ApplicationCRUD.create(db, **application_dict)
    return result

@router.get("/", response_model=list[ApplicationResponse])
def get_all_applications(
    db: Session = Depends(get_db),
    current_admin = Depends(get_current_admin)  # Требует JWT авторизацию
):
    """
    Получить все заявки с приоритизацией (сортировка по score DESC).
    Требует JWT авторизацию.
    """
    applications = ApplicationCRUD.get_all(db)
    
    # Пересчитываем score для всех заявок (на случай если алгоритм изменился)
    # и обновляем в БД, если score изменился
    for app in applications:
        new_score = calculate_priority_score(app)
        if app.priority_score != new_score:
            app.priority_score = new_score
            db.commit()
            db.refresh(app)
    
    # Сортировка по score (убывание)
    applications_sorted = sorted(applications, key=lambda x: x.priority_score or 0, reverse=True)
    
    return applications_sorted

@router.get("/{id}", response_model=ApplicationResponse)
def get_application(
    id: int,
    db: Session = Depends(get_db),
    current_admin = Depends(get_current_admin)  # Требует JWT авторизацию
):
    """Получить детали конкретной заявки (требует JWT авторизацию)"""
    application = db.query(Application).filter(Application.id == id).first()
    if not application:
        raise HTTPException(status_code=404, detail="Application not found")
    return application
