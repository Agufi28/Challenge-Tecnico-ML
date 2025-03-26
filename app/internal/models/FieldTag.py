
from sqlalchemy import ForeignKey

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from internal.models.Base import Base
from internal.models.DataTypeTag import DataTypeTag
class FieldTag(Base):
    __tablename__ = "field_tags"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    field_id: Mapped[int] = mapped_column(ForeignKey("table_fields.id"))
    tag_id: Mapped[int] = mapped_column(ForeignKey("datatype_tags.id"))
    certanty_score: Mapped[int] = mapped_column(nullable=False)

    tag: Mapped[DataTypeTag] = relationship()
    field: Mapped['DatabaseField'] = relationship(back_populates='tags')


    def __init__(self, field, tag, certanty_score):
        self.tag = tag
        self.field = field
        self.certanty_score = certanty_score