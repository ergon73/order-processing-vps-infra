"""
CREATE TABLE IF NOT EXISTS behavior_metrics (
    id SERIAL PRIMARY KEY,
    application_id INTEGER,  -- может быть NULL или 0 (НЕ FK для анонимных метрик!)
    time_on_page INTEGER,
    buttons_clicked TEXT,  -- JSON строка
    cursor_positions TEXT,  -- JSON строка
    return_frequency INTEGER DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);
"""

from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from core.database import Base

class BehaviorMetrics(Base):
    __tablename__ = "behavior_metrics"
    
    id = Column(Integer, primary_key=True, index=True)
    application_id = Column(Integer)  # Может быть NULL или 0 для анонимных метрик (НЕ FK!)
    time_on_page = Column(Integer)
    buttons_clicked = Column(String)  # JSON строка
    cursor_positions = Column(String)  # JSON строка
    return_frequency = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


# CRUD Operations
class BehaviorMetricsCRUD:
    @staticmethod
    def create(db, **kwargs):
        obj = BehaviorMetrics(**kwargs)
        db.add(obj)
        db.commit()
        db.refresh(obj)
        return obj
    
    @staticmethod
    def get_all(db):
        return db.query(BehaviorMetrics).all()
