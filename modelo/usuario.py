from pydantic import BaseModel, EmailStr, Field
from typing import Optional


class Usuario(BaseModel):
    id: Optional[str] = None
    nombre: str
    apellido: str
    email: EmailStr
    username: str
    password: str
