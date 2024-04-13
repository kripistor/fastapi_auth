import logging
import sys
from typing import List, Optional

import pytest
from pydantic import HttpUrl, PostgresDsn, field_validator
from pydantic.networks import AnyHttpUrl
from pydantic_core import MultiHostUrl
from pydantic_core.core_schema import FieldValidationInfo
from pydantic_settings import BaseSettings

logger = logging.getLogger(__name__)


class Settings(BaseSettings):
    PROJECT_NAME: str = "Auth Service"
    API_PATH: str = "/api/v1"
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []
    DATABASE_URL: PostgresDsn
    ASYNC_DATABASE_URL: Optional[PostgresDsn] = None

    @field_validator("ASYNC_DATABASE_URL")
    def build_async_database_url(cls, v: Optional[str], info: FieldValidationInfo):
        """Builds ASYNC_DATABASE_URL from DATABASE_URL."""
        url: MultiHostUrl | str = info.data.get("DATABASE_URL")
        url = str(url)
        return url.replace("postgresql", "postgresql+asyncpg", 1)

    SECRET_KEY: str
    AUTHJWT_SECRET_KEY: str
    #  END: required environment variables


settings = Settings()
