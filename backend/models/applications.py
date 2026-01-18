"""
CREATE TABLE IF NOT EXISTS applications (
    id SERIAL PRIMARY KEY,
    first_name TEXT,
    last_name TEXT,
    middle_name TEXT,
    business_info TEXT,
    budget TEXT,
    preferred_contact_method TEXT,
    comments TEXT,
    business_niche TEXT,
    company_size TEXT,
    task_scope TEXT,
    user_role TEXT,
    business_size TEXT,
    need_volume TEXT,
    deadline TEXT,
    task_type TEXT,
    interested_product TEXT,
    preferred_contact TEXT,
    convenient_time TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);
"""

from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from core.database import Base

class Application(Base):
    __tablename__ = "applications"
    
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String)
    last_name = Column(String)
    middle_name = Column(String)
    business_info = Column(String)
    budget = Column(String)
    preferred_contact_method = Column(String)
    comments = Column(String)
    business_niche = Column(String)
    company_size = Column(String)
    task_scope = Column(String)
    user_role = Column(String)
    business_size = Column(String)
    need_volume = Column(String)
    deadline = Column(String)
    task_type = Column(String)
    interested_product = Column(String)
    preferred_contact = Column(String)
    convenient_time = Column(String)
    priority_score = Column(Integer, default=0)  # Score приоритизации (0-100)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())


# CRUD Operations
class ApplicationCRUD:
    @staticmethod
    def create(db, **kwargs):
        obj = Application(**kwargs)
        db.add(obj)
        db.commit()
        db.refresh(obj)
        return obj
    
    @staticmethod
    def get_all(db):
        return db.query(Application).all()
