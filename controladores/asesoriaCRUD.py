from typing import List
from fastapi import HTTPException, APIRouter
from db.db import collection_asesorias
from modelo.asesoria import Asesoria

router = APIRouter()

@router.post("/", response_description="Crear una nueva asesoría", response_model=Asesoria)
async def create_asesoria(asesoria: Asesoria):
    existing_asesoria = await collection_asesorias.find_one({"titulo": asesoria.titulo, "fecha": asesoria.fecha})
    if existing_asesoria is not None:
        raise HTTPException(status_code=400, detail="La asesoría ya existe para esta fecha y título")
    result = await collection_asesorias.insert_one(asesoria.dict())
    asesoria.id = str(result.inserted_id)
    return asesoria

@router.get("/", response_description="Listar asesorías", response_model=List[Asesoria])
async def read_asesorias():
    asesorias = await collection_asesorias.find().to_list(100)
    for asesoria in asesorias:
        asesoria["id"] = str(asesoria["_id"])
    return asesorias

@router.get("/{id}", response_model=Asesoria)
async def find_asesoria_by_id(id: str):
    asesoria = await collection_asesorias.find_one({"_id": id})
    if asesoria:
        asesoria["id"] = str(asesoria["_id"])
        return asesoria
    raise HTTPException(status_code=404, detail="Asesoría no encontrada")

@router.put("/{id}", response_model=Asesoria)
async def update_asesoria(id: str, asesoria: Asesoria):
    updated_asesoria = await collection_asesorias.find_one_and_update(
        {"_id": id}, {"$set": asesoria.dict()}
    )
    if updated_asesoria:
        return asesoria
    raise HTTPException(status_code=404, detail="Asesoría no encontrada")

@router.delete("/{id}", response_model=Asesoria)
async def delete_asesoria(id: str):
    deleted_asesoria = await collection_asesorias.find_one_and_delete({"_id": id})
    if deleted_asesoria:
        deleted_asesoria["id"] = str(deleted_asesoria["_id"])
        return deleted_asesoria
    raise HTTPException(status_code=404, detail="Asesoría no encontrada")
