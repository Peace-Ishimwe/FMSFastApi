from datetime import datetime
from sqlalchemy import Column, String, Boolean, DateTime, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import validates
from passlib.hash import bcrypt
import enum

Base = declarative_base()

class RoleChoices(enum.Enum):
    Admin = "Admin"
    User = "User"

class ProvinceChoices(enum.Enum):
    kigali = "Kigali"
    northern = "Northern"
    southern = "Southern"
    eastern = "Eastern"
    western = "Western"

class SectorChoices(enum.Enum):
    Agriculture = "Agriculture"
    Trading = "Trading"

class CustomUser(Base):
    __tablename__ = "users"
    ...