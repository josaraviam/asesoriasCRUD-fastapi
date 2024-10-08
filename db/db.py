import certifi
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv

load_dotenv()

MONGO_URL = os.environ.get("MONGO_DB")

client = AsyncIOMotorClient(MONGO_URL, tlsCAFile=certifi.where())

database = client["ing_swii"]

collection_asesorias = database["asesorias"]
collection_usuarios = database["usuarios"]