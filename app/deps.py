from fastapi import Depends, HTTPException, status, Cookie
from app.core.auth import decode_token
from app.users.models import User
from app.core.database import get_db
from sqlalchemy.orm import Session

async def get_current_user(
    access_token: str|None = Cookie(default=None, alias="access_token"),
    db: Session = Depends(get_db)
) -> User:

    if access_token is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
        )

    payload = decode_token(access_token)
    if payload["type"] != "access":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token type",
        )
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
        )
    
    user = db.query(User).filter(User.id == int(payload["sub"])).first()
    if user is None:
        raise HTTPException(401, "User not found")

    return user