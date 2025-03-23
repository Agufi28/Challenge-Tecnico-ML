from sqlalchemy import String
from sqlalchemy import Enum
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from internal.models.Base import Base
from internal.models.FieldDataTypes import FieldDataTypes
from internal.models.ControlTag import ControlTag

class DatabaseField(Base):
    __tablename__ = "table_fields"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    # The maximum size of the column name is setted based on the MySQL specification. An extended value should be considered in case support for new database engines is added
    name: Mapped[str] = mapped_column(String(64), nullable=False) 
    type: Mapped[FieldDataTypes] = mapped_column(Enum(FieldDataTypes), nullable=False)
    
    table_id: Mapped[int] = mapped_column(ForeignKey("tables.id"))
    table = relationship("DatabaseTable", back_populates="fields")

    def __init__(self, name: str, type: FieldDataTypes):
        self.name = name
        self.type = FieldDataTypes
        self.dataSample = []

    def getName(self) -> str:
        return self.name
    
    def updateTags(self, tags: dict[ControlTag, int]) -> None:
        # TODO: Implement
        pass