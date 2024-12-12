from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional
from .models import ProvinceChoices, SectorChoices, RoleChoices

class CustomUserCreate(BaseModel):
    email: EmailStr
    first_name: str
    last_name: str
    phone: Optional[str]
    province: ProvinceChoices
    sector: SectorChoices
    role: Optional[RoleChoices] = RoleChoices.User
    password: str

class CustomUserRead(BaseModel):
    id: str
    email: EmailStr
    first_name: str
    last_name: str
    phone: Optional[str]
    province: ProvinceChoices
    sector: SectorChoices
    role: RoleChoices
    date_joined: datetime
    is_active: bool
    is_staff: bool

    class Config:
        orm_mode = True