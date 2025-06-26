from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import auth
from app.models.user import Base
from app.core.database import engine
from app.core.config import Settings
from loguru import logger
from app.core.limiter import limiter

# Add for rate limiting
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

# Set loguru log color to magenta (closest to violet)
logger.remove()
logger.add(lambda msg: print(msg, end=""), colorize=True, format="<magenta>{time:YYYY-MM-DD HH:mm:ss}</magenta> | <magenta>{level}</magenta> | <magenta>{message}</magenta>")

app = FastAPI(title="Auth Service")

# Rate limiter setup
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

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


# Email Confirmation: Add email verification for registration.

# Password Reset: Implement password reset flow.

# OAuth2: Support external login (Google, Facebook, etc.).
