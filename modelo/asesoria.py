from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class Asesoria(BaseModel):
    id: Optional[str] = None
    titulo: str
    descripcion: str
    fecha: datetime
    hora: str
    profesor: str
    usuario_id: str # Se me ocurre que podemos mostrar este en pantalla para simplificar

