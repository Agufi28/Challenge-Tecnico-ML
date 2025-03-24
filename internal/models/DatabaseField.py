from sqlalchemy import String
from sqlalchemy import Enum
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from internal.models.Base import Base
from internal.models.FieldDataTypes import FieldDataTypes
from internal.models.FieldTag import FieldTag

from internal.models.DataTypeTag import DataTypeTag

class DatabaseField(Base):
    __tablename__ = "table_fields"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    # The maximum size of the column name is setted based on the MySQL specification. An extended value should be considered in case support for new database engines is added
    name: Mapped[str] = mapped_column(String(64), nullable=False) 
    type: Mapped[FieldDataTypes] = mapped_column(Enum(FieldDataTypes), nullable=False)

    table_id: Mapped[int] = mapped_column(ForeignKey("schema_tables.id"))

    tags: Mapped[list[FieldTag]] = relationship()




    def __init__(self, name: str, type: FieldDataTypes):
        self.name = name
        self.type = FieldDataTypes
        self.dataSample = []

    def getName(self) -> str:
        return self.name
    
    def updateTag(self, tag: DataTypeTag, score: int) -> None:
        # TODO: Implement
        pass

    def removeUnfoundTags(self):
        #TODO: Implement
        pass