from sqlalchemy import Column ,Integer ,String , DateTime ,Enum, Boolean
from sqlalchemy.ext.declarative import declarative_base
import enum 
from datetime import datetime

Base = declarative_base()


class UserRole(str,enum.Enum):
    user ="user"
    vendor = "vendor"
    admin = "admin"

class User(Base):
    __tablename__ = "users"
    id = Column(Integer , primary_key = True,index = True)
    email =Column(String, unique =True ,index = True , nullable = False)
    hashed_password =Column(String , nullable = False)
    role = Column(Enum(UserRole),default=UserRole.user , nullable =False)
    created_at = Column(DateTime ,default = datetime.utcnow)
    is_verified = Column(Boolean, default=False, nullable=False)
    verification_code = Column(String, nullable=True)
