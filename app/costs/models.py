# Database models
from sqlalchemy import Column, Integer, String
from app.core.database import Base

class Cost(Base):
    __tablename__ = "costs"
    id = Column(Integer, primary_key=True, index=True)
    description = Column(String(30))
    amount = Column(Integer)