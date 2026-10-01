from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False, index=True)
    email = Column(String(100), unique=True, nullable=False, index=True)
    hashed_password = Column(String(255), nullable=False)  # هش نهایی در اینجا ذخیره می‌شود
    is_active = Column(Boolean, default=True)  # وضعیت فعال بودن کاربر

    cost = relationship("Cost", back_populates="user")
    
