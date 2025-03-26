import bcrypt

from datetime import datetime
from typing import Optional

from sqlalchemy import String

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from internal.models.Base import Base

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    username: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    # The size of this field is not arbitrary. It's ment to support hashes on the BCrypt format.
    _password_hash: Mapped[str] = mapped_column(String(72), nullable=False)
    is_admin: Mapped[bool] = mapped_column(nullable=False, default=False)
    last_login: Mapped[Optional[datetime]] = mapped_column(nullable=True)

    def __init__(self, username: str, password: str , isAdmin: bool):
        self.username = username
        self.is_admin = isAdmin
        # The password is stored in a hashed form from the moment the user is created.
        self._password_hash = bcrypt.hashpw(
            password.encode(), 
            bcrypt.gensalt()
        ).decode()
