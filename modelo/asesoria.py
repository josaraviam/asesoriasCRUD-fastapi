from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class Asesoria(BaseModel):
    id: Optional[str] = Field(None, description="Identificador único de la asesoría, generado automáticamente.")
    materia: str = Field(..., description="Materia de la asesoría.")
    tema: str = Field(..., description="Tema con el que necesitas ayuda.")
    fecha: datetime = Field(..., description="Fecha en la que se llevará a cabo la asesoría.")
    hora: str = Field(..., description="Hora de la asesoría, debe ser en formato HH:MM.")
    profesor: str = Field(..., description="Nombre del profesor que impartirá la asesoría.")
    usuario_id: str = Field(..., description="Identificador del usuario que solicita la asesoría.")
