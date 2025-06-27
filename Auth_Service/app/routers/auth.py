from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.user import (
    UserCreate, UserOut, Token, UserLogin, EmailVerification,
    PasswordResetRequest, PasswordReset
)
from app.services.user_service import (
    create_user, get_user_by_email, set_verification_code, generate_verification_code,
    set_password_reset_code, reset_user_password
)
from app.services.email_service import (
    send_verification_code_email, send_password_reset_code_email
)
from app.core.security import verify_password, create_access_token
from app.core.database import get_db
from loguru import logger
from slowapi.util import get_remote_address
from app.core.limiter import limiter  # Import limiter from core, not main

# Set loguru log color to magenta (closest to violet)
logger.remove()
logger.add(lambda msg: print(msg, end=""), colorize=True, format="<magenta>{time:YYYY-MM-DD HH:mm:ss}</magenta> | <magenta>{level}</magenta> | <magenta>{message}</magenta>")

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", response_model=UserOut, status_code=201)
@limiter.limit("5/minute")
async def register(user_in: UserCreate, db: AsyncSession = Depends(get_db), request: Request = None):
    logger.info(f"Register endpoint called for: {user_in.email}")
    existing = await get_user_by_email(db, user_in.email)
    if existing:
        logger.warning(f"Email already registered: {user_in.email}")
        raise HTTPException(status_code=400, detail="Email already register")
    user = await create_user(db, user_in)
    code = generate_verification_code()
    await set_verification_code(db, user, code)
    send_verification_code_email(user.email, code)
    logger.success(f"User registered: {user.email}, verification code sent.")
    return user

@router.post("/verify-email")
async def verify_email(data: EmailVerification, db: AsyncSession = Depends(get_db)):
    user = await get_user_by_email(db, data.email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if user.is_verified:
        return {"message": "Email already verified."}
    if user.verification_code != data.code:
        raise HTTPException(status_code=400, detail="Invalid verification code")
    user.is_verified = True
    user.verification_code = None
    await db.commit()
    return {"message": "Email verified successfully."}

@router.post("/login", response_model=Token)
@limiter.limit("10/minute")
async def login(user_in: UserLogin, db: AsyncSession = Depends(get_db), request: Request = None):
    logger.info(f"Login endpoint called for: {user_in.email}")
    user = await get_user_by_email(db, user_in.email)
    if not user or not verify_password(user_in.password, user.hashed_password):
        logger.warning(f"Login failed for: {user_in.email}")
        raise HTTPException(status_code=401, detail="Incorrect email or password")
    token = create_access_token({"sub": str(user.id), "role": user.role})
    logger.success(f"Login successful for: {user_in.email}")
    return Token(access_token=token)

@router.post("/request-password-reset")
async def request_password_reset(data: PasswordResetRequest, db: AsyncSession = Depends(get_db)):
    user = await get_user_by_email(db, data.email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    code = generate_verification_code()
    await set_password_reset_code(db, user, code)
    send_password_reset_code_email(user.email, code)
    logger.info(f"Password reset code sent to {user.email}")
    return {"message": "Password reset code sent to your email."}

@router.post("/reset-password")
async def reset_password(data: PasswordReset, db: AsyncSession = Depends(get_db)):
    user = await get_user_by_email(db, data.email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if user.password_reset_code != data.code:
        raise HTTPException(status_code=400, detail="Invalid reset code")
    await reset_user_password(db, user, data.new_password)
    logger.success(f"Password reset for {user.email}")
    return {"message": "Password has been reset successfully."}
