
from sqlalchemy import ForeignKey

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from internal.models.Base import Base
#from internal.models.DataTypeTag import DataTypeTag

class ControlAffectedTag(Base):
    __tablename__ = "control_affected_tags"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    control_id: Mapped[int] = mapped_column(ForeignKey("controls.id"))
    tag_id: Mapped[int] = mapped_column(ForeignKey("datatype_tags.id"))
    affect_score_by: Mapped[int] = mapped_column(nullable=False)
    tag = relationship("DataTypeTag")
    control = relationship("Control")


    def __init__(self, control, tag, affectedScoreBy):
        self.control = control
        self.tag = tag
        self.affect_score_by = affectedScoreBy