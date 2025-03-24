from typing import Optional
from sqlalchemy import String

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from internal.models.Base import Base

class DataTypeTag(Base):
    __tablename__ = "datatype_tags"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(32), nullable=False) 
    description: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)


    affectedByControls = relationship("ControlAffectedTag", back_populates="tag")
    detectedOnFields = relationship("FieldTag", back_populates="tag")

    def __init__(self, name):
        self.name = name