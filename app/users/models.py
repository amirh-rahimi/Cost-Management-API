from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from passlib.context import CryptContext
from app.core.database import Base

# ۲. تنظیم Context هش (با الگوریتم bcrypt)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False, index=True)
    email = Column(String(100), unique=True, nullable=False, index=True)
    hashed_password = Column(String(255), nullable=False)  # هش نهایی در اینجا ذخیره می‌شود
    is_active = Column(Boolean, default=True)  # وضعیت فعال بودن کاربر

    cost = relationship("Cost", back_populates="user")
    
    def set_password(self, plain_password: str) -> None:
        self.hashed_password = pwd_context.hash(plain_password)

    def verify_password(self, plain_password: str) -> bool:
        return pwd_context.verify(plain_password, self.hashed_password)
