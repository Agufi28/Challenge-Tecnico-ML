from datetime import datetime
from typing import Optional
from sqlalchemy import ForeignKey, String

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from internal.models.Base import Base
from internal.models.User import User

class DataTypeTag(Base):
    __tablename__ = "datatype_tags"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(32), nullable=False) 
    description: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    created_by_id: Mapped[Optional[int]] = mapped_column(ForeignKey("users.id"))
    createdBy: Mapped[Optional[User]] = relationship()
    created_at: Mapped[datetime] = mapped_column(default=datetime.now())

    def __init__(self, name: str, description: str=None, createdBy: User=None):
        self.name = name
        self.description = description
        self.createdBy = createdBy