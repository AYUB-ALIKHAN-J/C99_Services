from fastapi import FastAPI
from app.routers import auth
from app.models.user import Base
from app.core.database import engine
from loguru import logger

# Set loguru log color to magenta (closest to violet)
logger.remove()
logger.add(lambda msg: print(msg, end=""), colorize=True, format="<magenta>{time:YYYY-MM-DD HH:mm:ss}</magenta> | <magenta>{level}</magenta> | <magenta>{message}</magenta>")

app = FastAPI(title="Auth Service")

# Routers
app.include_router(auth.router)

# Create tables on startup (for dev only; use Alembic for prod)
@app.on_event("startup")
async def on_startup():
    logger.info("Starting up and creating tables if needed...")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    logger.success("Startup complete.")





# CORS: Configure allowed origins in FastAPI.

# Rate Limiting: Protect endpoints from brute-force attacks.

# Email Confirmation: Add email verification for registration.

# Password Reset: Implement password reset flow.

# OAuth2: Support external login (Google, Facebook, etc.).
