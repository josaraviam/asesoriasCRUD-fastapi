from bson import ObjectId
from typing import List
from fastapi import HTTPException, APIRouter
from db.db import collection_asesorias
from modelo.asesoria import Asesoria

router = APIRouter()

@router.post("/", response_description="Crear una nueva asesoría", response_model=Asesoria)
async def create_asesoria(asesoria: Asesoria):
    # Verificar si el usuario ya tiene una asesoría a la misma hora y fecha
    existing_asesoria = await collection_asesorias.find_one({
        "usuario_id": asesoria.usuario_id,
        "fecha": asesoria.fecha,
        "hora": asesoria.hora
    })
    if existing_asesoria is not None:
        raise HTTPException(status_code=400, detail="Ya existe una asesoría para este usuario a la misma hora y fecha")
    # Insertar la nueva asesoría en la base de datos
    result = await collection_asesorias.insert_one(asesoria.dict())
    asesoria.id = str(result.inserted_id)  # Convertir el ObjectId en string para el ID de la respuesta
    return asesoria

@router.get("/", response_description="Listar asesorías", response_model=List[Asesoria])
async def read_asesorias():
    asesorias = await collection_asesorias.find().to_list(100)
    for asesoria in asesorias:
        asesoria["id"] = str(asesoria["_id"])  # Convertir ObjectId a string para cada asesoría
    return asesorias

@router.get("/{id}", response_model=Asesoria)
async def find_asesoria_by_id(id: str):
    try:
        asesoria = await collection_asesorias.find_one({"_id": ObjectId(id)})
        if asesoria:
            asesoria["id"] = str(asesoria["_id"])  # Convertir ObjectId a string para la asesoría encontrada
            return asesoria
        raise HTTPException(status_code=404, detail="Asesoría no encontrada")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))  # Manejo de excepciones para errores inesperados

@router.put("/{id}", response_model=Asesoria)
async def update_asesoria(id: str, asesoria: Asesoria):
    try:
        updated_asesoria = await collection_asesorias.find_one_and_update(
            {"_id": ObjectId(id)}, {"$set": asesoria.dict()}, return_document=True
        )
        if updated_asesoria:
            return updated_asesoria  # Devolver la asesoría actualizada
        raise HTTPException(status_code=404, detail="Asesoría no encontrada")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))  # Manejo de excepciones para errores inesperados

@router.delete("/{id}", response_model=Asesoria)
async def delete_asesoria(id: str):
    try:
        deleted_asesoria = await collection_asesorias.find_one_and_delete({"_id": ObjectId(id)})
        if deleted_asesoria:
            deleted_asesoria["id"] = str(deleted_asesoria["_id"])  # Convertir ObjectId a string para la asesoría eliminada
            return deleted_asesoria
        raise HTTPException(status_code=404, detail="Asesoría no encontrada")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))  # Manejo de excepciones para errores inesperados

