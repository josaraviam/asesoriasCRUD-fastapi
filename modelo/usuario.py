from pydantic import BaseModel, EmailStr, Field
from typing import Optional


class Usuario(BaseModel):
    id: Optional[str] = Field(None, alias="_id")
    nombre: str
    apellido: str
    email: EmailStr
    username: str
    password: str
