"""
CREATE TABLE IF NOT EXISTS behavior_metrics (
    id SERIAL PRIMARY KEY,
    application_id INTEGER REFERENCES applications(id),
    time_on_page INTEGER,
    buttons_clicked TEXT,
    cursor_hovers TEXT,
    return_visits INTEGER,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);
"""

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from core.database import Base

class BehaviorMetrics(Base):
    __tablename__ = "behavior_metrics"
    
    id = Column(Integer, primary_key=True, index=True)
    application_id = Column(Integer, ForeignKey("applications.id"))
    time_on_page = Column(Integer)
    buttons_clicked = Column(String)
    cursor_hovers = Column(String)
    return_visits = Column(Integer)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
