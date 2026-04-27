from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from core.config import settings
from models.schemas import document_models

async def init_db():
    # Create Motor client
    client = AsyncIOMotorClient(settings.MONGODB_URL)
    
    # Initialize beanie with the engine and the list of models
    await init_beanie(
        database=client[settings.DATABASE_NAME],
        document_models=document_models
    )
    
    # Create default roles if they don't exist (Optional safety)
    from models.schemas import UserRole
    roles = ["admin", "user"]
    for role_name in roles:
        existing = await UserRole.find_one(UserRole.nombre_rol == role_name)
        if not existing:
            await UserRole(nombre_rol=role_name).create()
