from sqlalchemy.ext.asyncio import AsyncSession,create_async_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import Settings
from loguru import logger

DATABASE_URL = (
    f"postgresql+asyncpg://{Settings.POSTGRES_USER}:{Settings.POSTGRES_PASSWORD}"
    f"@{Settings.POSTGRES_HOST}:{Settings.POSTGRES_PORT}/{Settings.POSTGRES_DB}"
)
logger.info(f"DATABASE_URL: {DATABASE_URL}")

engine = create_async_engine(DATABASE_URL,echo=True)
logger.info("Async engine created.")

AsyncSessionLocal = sessionmaker(engine,class_=AsyncSession,expire_on_commit =False)


async def get_db():
    async with AsyncSessionLocal() as session :
        yield session