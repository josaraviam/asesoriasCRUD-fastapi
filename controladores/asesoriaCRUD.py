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
    print(f"Intentando actualizar la asesoría con ID: {id}")  # Depuración para seguir el proceso de actualización
    try:
        # Verificar si existe alguna otra asesoría para este usuario, fecha y hora, excluyendo la asesoría actual
        existing_asesoria = await collection_asesorias.find_one({
            "_id": {"$ne": ObjectId(id)},  # Excluye la asesoría que se está actualizando
            "usuario_id": asesoria.usuario_id,
            "fecha": asesoria.fecha,
            "hora": asesoria.hora
        })
        if existing_asesoria:
            # Si se encuentra una asesoría duplicada, se impide la actualización y se retorna un error
            print("Conflicto: Ya existe otra asesoría para este usuario a la misma hora y fecha")
            raise HTTPException(status_code=400, detail="Ya existe una asesoría para este usuario a la misma hora y fecha")

        # Actualizar la asesoría si no se encontró duplicado
        updated_asesoria = await collection_asesorias.find_one_and_update(
            {"_id": ObjectId(id)},
            {"$set": asesoria.dict()},
            return_document=True  # Configuración para que MongoDB devuelva el documento actualizado
        )
        if updated_asesoria:
            print(f"Asesoría actualizada exitosamente: {updated_asesoria}")  # Confirmación de la actualización
            return updated_asesoria
        else:
            # Si no se encuentra la asesoría, se retorna un error indicando que no se encontró
            print("No se encontró la asesoría con el ID proporcionado para actualizar")
            raise HTTPException(status_code=404, detail="Asesoría no encontrada")
    except Exception as e:
        # Manejo de cualquier otro tipo de error durante la actualización
        print(f"Error durante la actualización: {e}")
        raise HTTPException(status_code=500, detail=str(e))

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
