# api/routes/auth.py
#
# NOTE: Not in the original plan — needed because main.py imports it.
# Cadastro e login básicos usando os modelos e a segurança já existentes.
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel, EmailStr

from core.database import get_db
from core.security import hash_password, verify_password, create_access_token
from models.user import User

router = APIRouter()


class RegisterInput(BaseModel):
    email: EmailStr
    name: str
    password: str


class TokenOutput(BaseModel):
    access_token: str
    token_type: str = "bearer"


@router.post("/register", response_model=TokenOutput)
async def register(data: RegisterInput, db: AsyncSession = Depends(get_db)):
    existing = await db.execute(select(User).where(User.email == data.email))
    if existing.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Email já cadastrado")

    user = User(
        email=data.email,
        name=data.name,
        hashed_password=hash_password(data.password),
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)

    token = create_access_token(subject=str(user.id))
    return TokenOutput(access_token=token)


@router.post("/login", response_model=TokenOutput)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.email == form_data.username))
    user = result.scalar_one_or_none()

    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email ou senha incorretos",
        )

    token = create_access_token(subject=str(user.id))
    return TokenOutput(access_token=token)
