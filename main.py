from fastapi import FastAPI, HTTPException
from db.db import client
from controladores.asesoriaCRUD import router as asesorias_router

app = FastAPI()
app.include_router(asesorias_router, tags=["asesorias"], prefix="/asesorias")

@app.get("/")
async def read_root():
    return {"message": "Bienvenido a la API de Asesorías"}

@app.on_event("shutdown")
def shutdown_db_client():
    client.close()
