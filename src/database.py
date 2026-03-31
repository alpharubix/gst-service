from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient
from src.config import settings
from src.models.gst_reference import GstReference
from src.logger import get_logger


logger = get_logger(__name__)
db_client: AsyncIOMotorClient = None

async def connect_db():
    global db_client
    db_client = AsyncIOMotorClient(settings.MONGODB_URL)
    await db_client.admin.command("ping")  # test the connection
    logger.info("MongoDB connected!")
    await init_beanie(
        database=db_client[settings.MONGODB_DB_NAME],
        document_models=[GstReference]  # we'll add models here 
    )
    logger.info(f"Beanie ready — DB: {settings.MONGODB_DB_NAME}")

async def close_db():
    global db_client
    if db_client:
        db_client.close()
        logger.info("MongoDB disconnected")