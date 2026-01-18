"""
CREATE TABLE IF NOT EXISTS admin_settings (
    id SERIAL PRIMARY KEY,
    services TEXT NOT NULL,
    budget_range TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);
"""

from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from core.database import Base

class AdminSettings(Base):
    __tablename__ = "admin_settings"
    
    id = Column(Integer, primary_key=True, index=True)
    services = Column(String, nullable=False)
    budget_range = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())


# CRUD Operations
class AdminSettingsCRUD:
    @staticmethod
    def create(db, services: str, budget_range: str):
        obj = AdminSettings(services=services, budget_range=budget_range)
        db.add(obj)
        db.commit()
        db.refresh(obj)
        return obj
    
    @staticmethod
    def get_latest(db):
        return db.query(AdminSettings).order_by(AdminSettings.id.desc()).first()
    
    @staticmethod
    def get_all(db):
        return db.query(AdminSettings).all()
