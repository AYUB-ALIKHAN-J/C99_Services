from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.user import User, UserRole
from app.schemas.user import UserCreate
from app.core.security import get_password_hash
from loguru import logger

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

