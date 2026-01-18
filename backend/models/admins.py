from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from core.database import Base

class Admin(Base):
    __tablename__ = "admins"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, nullable=False, index=True)
    hashed_password = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

# CRUD Operations
class AdminCRUD:
    @staticmethod
    def create(db, **kwargs):
        obj = Admin(**kwargs)
        db.add(obj)
        db.commit()
        db.refresh(obj)
        return obj
    
    @staticmethod
    def get_by_email(db, email: str):
        return db.query(Admin).filter(Admin.email == email).first()
    
    @staticmethod
    def get_all(db):
        return db.query(Admin).all()
    
    @staticmethod
    def count(db):
        return db.query(Admin).count()
