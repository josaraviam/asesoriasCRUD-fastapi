from fastapi import FastAPI, HTTPException
from db.db import client
from controladores.asesoriaCRUD import router as asesorias_router
from controladores.usuarioCRUD import router as usuarios_router  # Importa el router de usuarios

app = FastAPI()
app.include_router(asesorias_router, tags=["asesorias"], prefix="/asesorias")
app.include_router(usuarios_router, tags=["usuarios"], prefix="/usuarios")  # Incluye el router de usuarios

@app.get("/")
async def read_root():
    return {"message": "Bienvenido a la API de Asesorías"}

@app.on_event("shutdown")
def shutdown_db_client():
    client.close()
