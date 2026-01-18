from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from core.database import get_db
from models.behavior_metrics import BehaviorMetrics, BehaviorMetricsCRUD
from routes.auth import get_current_admin

router = APIRouter(prefix="/behavior-metrics", tags=["Behavior Metrics"])

class BehaviorMetricsCreate(BaseModel):
    application_id: Optional[int] = 0  # Может быть 0 для анонимных метрик
    time_on_page: int
    buttons_clicked: str  # JSON строка
    cursor_positions: str  # JSON строка
    return_frequency: int = 0

class BehaviorMetricsResponse(BaseModel):
    id: int
    application_id: Optional[int]
    time_on_page: int
    created_at: datetime
    
    class Config:
        from_attributes = True

@router.post("/", response_model=BehaviorMetricsResponse, status_code=201)
def create_metrics(data: BehaviorMetricsCreate, db: Session = Depends(get_db)):
    """
    Принимает поведенческие метрики и записывает в БД.
    ВАЖНО: application_id может быть 0 или null - это нормально для анонимных метрик.
    """
    # Преобразуем 0 в None для корректного хранения в БД
    metrics_data = data.model_dump()
    if metrics_data.get('application_id') == 0:
        metrics_data['application_id'] = None
    
    result = BehaviorMetricsCRUD.create(db, **metrics_data)
    return result

@router.get("/stats")
def get_metrics_stats(db: Session = Depends(get_db), current_admin = Depends(get_current_admin)):
    """
    Возвращает агрегированную статистику:
    - Среднее время на странице (день/неделя/месяц)
    - Топ координат курсора для heatmap
    """
    from datetime import timedelta
    from sqlalchemy import func
    
    now = datetime.utcnow()
    
    # Среднее время на странице за день
    day_ago = now - timedelta(days=1)
    avg_day = db.query(func.avg(BehaviorMetrics.time_on_page)).filter(
        BehaviorMetrics.created_at >= day_ago
    ).scalar() or 0
    
    # Среднее время на странице за неделю
    week_ago = now - timedelta(days=7)
    avg_week = db.query(func.avg(BehaviorMetrics.time_on_page)).filter(
        BehaviorMetrics.created_at >= week_ago
    ).scalar() or 0
    
    # Среднее время на странице за месяц
    month_ago = now - timedelta(days=30)
    avg_month = db.query(func.avg(BehaviorMetrics.time_on_page)).filter(
        BehaviorMetrics.created_at >= month_ago
    ).scalar() or 0
    
    # Получаем все cursor_positions для heatmap (последние 1000 записей)
    recent_metrics = db.query(BehaviorMetrics.cursor_positions).filter(
        BehaviorMetrics.cursor_positions.isnot(None),
        BehaviorMetrics.created_at >= month_ago
    ).order_by(BehaviorMetrics.created_at.desc()).limit(1000).all()
    
    # Парсим JSON строки и собираем координаты
    import json
    all_coordinates = []
    for (positions_str,) in recent_metrics:
        try:
            if positions_str:
                positions = json.loads(positions_str)
                if isinstance(positions, list):
                    all_coordinates.extend(positions)
        except (json.JSONDecodeError, TypeError):
            continue
    
    return {
        "average_time_on_page": {
            "day": round(avg_day, 2),
            "week": round(avg_week, 2),
            "month": round(avg_month, 2)
        },
        "heatmap_coordinates": all_coordinates[:1000]  # Ограничиваем для производительности
    }
