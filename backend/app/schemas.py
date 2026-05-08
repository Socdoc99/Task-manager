from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


# --- Schemas de Usuario ---

class UserCreate(BaseModel):
    """Lo que el frontend manda para registrarse"""
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    """Lo que el backend devuelve (nunca la contraseña)"""
    id: int
    email: str
    created_at: datetime

    class Config:
        from_attributes = True


# --- Schemas de Tarea ---

class TaskCreate(BaseModel):
    """Lo que el frontend manda para crear una tarea"""
    title: str
    description: Optional[str] = None

class TaskUpdate(BaseModel):
    """Todos opcionales — solo actualiza lo que llega"""
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None

class TaskResponse(BaseModel):
    """Lo que el backend devuelve"""
    id: int
    title: str
    description: Optional[str]
    completed: bool
    created_at: datetime
    owner_id: int

    class Config:
        from_attributes = True


# --- Schema de Auth ---

class Token(BaseModel):
    """El token JWT que devuelve el login"""
    access_token: str
    token_type: str