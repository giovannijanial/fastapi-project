from pydantic_settings import BaseSettings
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm.decl_api import DeclarativeMeta
from fastapi.templating import Jinja2Templates
from pathlib import Path
from typing import ClassVar

DBBaseModel = declarative_base()

class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    DB_URL: str = "postgresql+asyncpg://giovannijanial:123@localhost:5432/university"
    DBBaseModel: ClassVar[DeclarativeMeta] = DBBaseModel
    TEMPLATES: ClassVar[Jinja2Templates] = Jinja2Templates(directory="templates")
    MEDIA: ClassVar[Path] = Path("media")

    class Config:
        case_sensitive = True

settings = Settings()
