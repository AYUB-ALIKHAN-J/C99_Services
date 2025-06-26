from fastapi import FastAPI
from app.routers import auth
from app.models.user import Base
from app.core.database import engine
from loguru import logger

app = FastAPI(title="Auth Service")

# Routers
app.include_router(auth.router)

# Create tables on startup (for dev only; use Alembic for prod)
@app.on_event("startup")
async def on_startup():
    logger.info("Starting up and creating tables if needed...")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    logger.info("Startup complete.")
