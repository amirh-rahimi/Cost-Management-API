from fastapi import Depends, HTTPException, status, APIRouter, Response, Cookie
from .models import User
from sqlalchemy.orm import Session
from app.core.database import get_db
from .schemas import RegisterSchema, LoginSchema
from app.core.auth import hash_password, verify_password, create_access_token, create_refresh_token, decode_token,ACCESS_TOKEN_EXPIRE_MINUTES, REFRESH_TOKEN_EXPIRE_DAYS

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)


@router.post("/register", response_model=dict[str,str], status_code=status.HTTP_201_CREATED)
async def register(data: RegisterSchema, db: Session = Depends(get_db)):

    if db.query(User).filter(User.username == data.username).first():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="This username has already been taken.")
    if db.query(User).filter(User.email == data.email).first():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="This email has already been registered.")

    user = User(
        username=data.username,
        email=data.email,
        hashed_password=hash_password(data.password))

    db.add(user)
    db.commit()
    db.refresh(user)

    return {"msg": "Successful registration"}



@router.post("/login", response_model=dict[str, str])
async def login(
    data: LoginSchema,
    response: Response,
    db: Session = Depends(get_db),
    ):
    
    user = db.query(User).filter(User.username == data.username).one_or_none()
    if user is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid username")

    if not verify_password(data.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid password")

    access_token = create_access_token(user.id)
    refresh_token = create_refresh_token(user.id)

    response.set_cookie(
        key="access_token",
        value=access_token,
        max_age=ACCESS_TOKEN_EXPIRE_MINUTES*60,
        httponly=True
    )

    response.set_cookie(
    key="refresh_token",
    value=refresh_token,
    max_age=REFRESH_TOKEN_EXPIRE_DAYS * 24 * 60 * 60,
    httponly=True,
    path="/auth/refresh"
    )

    return {"msg": "Login successful."}

@router.post("/refresh", response_model=dict[str,str])
async def refresh(response: Response ,token: str|None = Cookie(default=None, alias="refresh_token")):
    payload = decode_token(token=token)
    if payload is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token")

    access_token = create_access_token(user_id=int(payload["sub"]))
    response.set_cookie(
            key="access_token",
            value=access_token,
            max_age=ACCESS_TOKEN_EXPIRE_MINUTES*60,
            httponly=True
        )

    return {"msg": "Access was created"}
