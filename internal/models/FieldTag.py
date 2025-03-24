
from sqlalchemy import ForeignKey

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from internal.models.Base import Base

class FieldTag(Base):
    __tablename__ = "field_tags"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    field_id: Mapped[int] = mapped_column(ForeignKey("table_fields.id"))
    tag_id: Mapped[int] = mapped_column(ForeignKey("datatype_tags.id"))

    certanty_score: Mapped[int] = mapped_column(nullable=False)

    field = relationship("DatabaseField", back_populates="tags")
    tag = relationship("DataTypeTag", back_populates="detectedOnFields")