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
    PROJECT_NAME: str = "porsche-website"

    SENTRY_DSN: Optional[HttpUrl] = None

    API_PATH: str = "/api/v1"

    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30 * 24 * 60  # 30 days

    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []

    # The following variables need to be defined in environment

    TEST_DATABASE_URL: Optional[PostgresDsn] = None
    DATABASE_URL: PostgresDsn
    ASYNC_DATABASE_URL: Optional[PostgresDsn] = None

    @field_validator("DATABASE_URL")
    def build_test_database_url(cls, v: Optional[str], info: FieldValidationInfo):
        """Overrides DATABASE_URL with TEST_DATABASE_URL in test environment."""
        if pytest in sys.modules:
            if v:
                url: MultiHostUrl = info.data.get("TEST_DATABASE_URL")
                if url:
                    return str(url.scheme.replace("postgres://", "postgresql://"))
                else:
                    raise ValueError("TEST_DATABASE_URL is not set")
        return v

    @field_validator("ASYNC_DATABASE_URL")
    def build_async_database_url(cls, v: Optional[str], info: FieldValidationInfo):
        """Builds ASYNC_DATABASE_URL from DATABASE_URL."""
        url: MultiHostUrl | str = info.data.get("DATABASE_URL")
        url = str(url)
        return url.replace("postgresql", "postgresql+asyncpg", 1)

    SECRET_KEY: str
    #  END: required environment variables


settings = Settings()