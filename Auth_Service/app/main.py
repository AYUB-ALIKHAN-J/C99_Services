from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import auth
from app.models.user import Base
from app.core.database import engine
from app.core.config import Settings
from loguru import logger

# Set loguru log color to magenta (closest to violet)
logger.remove()
logger.add(lambda msg: print(msg, end=""), colorize=True, format="<magenta>{time:YYYY-MM-DD HH:mm:ss}</magenta> | <magenta>{level}</magenta> | <magenta>{message}</magenta>")

app = FastAPI(title="Auth Service")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=Settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(auth.router)

# Create tables on startup (for dev only; use Alembic for prod)
@app.on_event("startup")
async def on_startup():
    logger.info("Starting up and creating tables if needed...")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    logger.success("Startup complete.")







# Rate Limiting: Protect endpoints from brute-force attacks.

# Email Confirmation: Add email verification for registration.

# Password Reset: Implement password reset flow.

# OAuth2: Support external login (Google, Facebook, etc.).
