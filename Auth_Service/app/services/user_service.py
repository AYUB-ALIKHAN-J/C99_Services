from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.user import User, UserRole
from app.schemas.user import UserCreate
from app.core.security import get_password_hash
from loguru import logger
import random
import string

# Set loguru log color to magenta (closest to violet)
logger.remove()
logger.add(lambda msg: print(msg, end=""), colorize=True, format="<magenta>{time:YYYY-MM-DD HH:mm:ss}</magenta> | <magenta>{level}</magenta> | <magenta>{message}</magenta>")

async def get_user_by_email(db:AsyncSession,email:str):
    logger.info(f"Looking up user by email: {email}")
    result = await db.execute(select(User).where(User.email==email))
    user = result.scalar()  # or result.first() if you want the whole row
    logger.info(f"User found: {user}")
    return user

async def create_user(db:AsyncSession,user_in:UserCreate):
    logger.info(f"Creating user: {user_in.email}")
    hashed_pw = get_password_hash(user_in.password)
    user = User(email = user_in.email,hashed_password = hashed_pw,role =user_in.role)
    db.add(user)
    await db.commit()
    await db.refresh(user)
    logger.success(f"User created: {user.id}")
    return user

async def set_verification_code(db: AsyncSession, user: User, code: str):
    user.verification_code = code
    await db.commit()
    await db.refresh(user)
    return user

def generate_verification_code(length=6):
    return ''.join(random.choices(string.digits, k=length))

async def set_password_reset_code(db: AsyncSession, user: User, code: str):
    user.password_reset_code = code
    await db.commit()
    await db.refresh(user)
    return user

async def reset_user_password(db: AsyncSession, user: User, new_password: str):
    user.hashed_password = get_password_hash(new_password)
    user.password_reset_code = None
    await db.commit()
    await db.refresh(user)
    return user

