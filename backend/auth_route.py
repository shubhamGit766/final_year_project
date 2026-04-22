from fastapi import APIRouter
from pydantic import BaseModel, EmailStr
from auth_controller import register_user, login_user, update_profile

router = APIRouter()


class RegisterRequest(BaseModel):
    name: str
    email: EmailStr
    password: str


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class ProfileRequest(BaseModel):
    user_id: str
    role: str
    level: str


@router.post("/register")
async def register(body: RegisterRequest):
    return await register_user(body.name, body.email, body.password)


@router.post("/login")
async def login(body: LoginRequest):
    return await login_user(body.email, body.password)


@router.put("/profile")
async def profile(body: ProfileRequest):
    return await update_profile(body.user_id, body.role, body.level)