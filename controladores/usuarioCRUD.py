from bson import ObjectId
from typing import List
from fastapi import HTTPException, APIRouter
from db.db import collection_usuarios
from modelo.usuario import Usuario
import bcrypt

router = APIRouter()


@router.post("/", response_description="Crear un nuevo usuario", response_model=Usuario)
async def create_usuario(usuario: Usuario):
    # Verificar si el email o username ya existe
    if await collection_usuarios.find_one({"email": usuario.email}):
        raise HTTPException(status_code=400, detail="El email ya está en uso")
    if await collection_usuarios.find_one({"username": usuario.username}):
        raise HTTPException(status_code=400, detail="El nombre de usuario ya está en uso")
    # Hash de la contraseña
    usuario.password = bcrypt.hashpw(usuario.password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    result = await collection_usuarios.insert_one(usuario.dict())
    usuario.id = str(result.inserted_id)
    return usuario


@router.get("/", response_description="Listar usuarios", response_model=List[Usuario])
async def read_usuarios():
    usuarios = await collection_usuarios.find().to_list(100)
    for usuario in usuarios:
        usuario["id"] = str(usuario["_id"])
    return usuarios


@router.get("/id/{id}", response_model=Usuario)
async def find_usuario_by_id(id: str):
    usuario = await collection_usuarios.find_one({"_id": ObjectId(id)})
    if usuario:
        usuario["id"] = str(usuario["_id"])
        return usuario
    raise HTTPException(status_code=404, detail="Usuario no encontrado")


@router.get("/username/{username}", response_model=Usuario)
async def find_id_by_username(username: str):
    usuario = await collection_usuarios.find_one({"username": username})
    if usuario:
        return str(usuario["_id"])
    raise HTTPException(status_code=404, detail="Usuario no encontrado")


@router.put("/{id}", response_model=Usuario)
async def update_usuario(id: str, usuario: Usuario):
    result = await collection_usuarios.find_one_and_update(
        {"_id": ObjectId(id)},
        {"$set": usuario.dict()},
        return_document=True
    )
    if result:
        return result
    raise HTTPException(status_code=404, detail="Usuario no encontrado")


@router.delete("/{id}")
async def delete_usuario(id: str):
    result = await collection_usuarios.delete_one({"_id": ObjectId(id)})
    if result.deleted_count == 1:
        return {"message": "Usuario eliminado correctamente"}
    raise HTTPException(status_code=404, detail="Usuario no encontrado")
