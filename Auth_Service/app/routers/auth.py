from fastapi import APIRouter, Depends, HTTPException , status
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.user import UserCreate , UserOut , Token ,UserLogin
from app.services.user_service import create_user , get_user_by_email 
from app.core.security import verify_password , create_access_token
from app.core.database import get_db
from loguru import logger

# Set loguru log color to magenta (closest to violet)
logger.remove()
logger.add(lambda msg: print(msg, end=""), colorize=True, format="<magenta>{time:YYYY-MM-DD HH:mm:ss}</magenta> | <magenta>{level}</magenta> | <magenta>{message}</magenta>")

router = APIRouter(prefix="/auth",tags=["auth"])

@router.post("/register" , response_model=UserOut,status_code=201)
async def register(user_in:UserCreate, db: AsyncSession=Depends(get_db)):
    logger.info(f"Register endpoint called for: {user_in.email}")
    existing = await get_user_by_email(db , user_in.email)
    if existing:
        logger.warning(f"Email already registered: {user_in.email}")
        raise HTTPException(status_code=400 ,detail="Email already register")
    user = await create_user(db ,user_in)
    logger.success(f"User registered: {user.email}")
    return user

@router.post("/login", response_model=Token)
async def login(user_in: UserLogin, db: AsyncSession = Depends(get_db)):
    logger.info(f"Login endpoint called for: {user_in.email}")
    user = await get_user_by_email(db, user_in.email)
    if not user or not verify_password(user_in.password, user.hashed_password):
        logger.warning(f"Login failed for: {user_in.email}")
        raise HTTPException(status_code=401, detail="Incorrect email or password")
    token = create_access_token({"sub": str(user.id), "role": user.role})
    logger.success(f"Login successful for: {user_in.email}")
    return Token(access_token=token)
