from pydantic import BaseModel, EmailStr, Field

class BaseAuth(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    password: str

class RegisterSchema(BaseAuth):
    email: EmailStr

    class Config:
        from_attributes = True

class LoginSchema(BaseAuth):
    pass