from fastapi import APIRouter, Depends
from .models import User
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.deps import get_current_user
from .schemas import BaseUser

router = APIRouter(prefix="/user", tags=["user"])

@router.get("/me", response_model=BaseUser)
async def get_me(user: User = Depends(get_current_user)):
    return user