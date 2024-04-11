from typing import TYPE_CHECKING

from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTableUUID

from app.db import Base

if TYPE_CHECKING:
    from app.models.item import Item  # noqa: F401


class User(SQLAlchemyBaseUserTableUUID, Base):
    __tablename__ = "users"

    def __repr__(self):
        return f"User(id={self.id!r}, name={self.email!r})"
