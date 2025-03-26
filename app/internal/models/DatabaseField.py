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

    tags: Mapped[list[FieldTag]] = relationship(cascade="all, delete-orphan")


    def __init__(self, name: str, type: FieldDataTypes):
        self.name = name
        self.type = type
        self.dataSample = []

    def getName(self) -> str:
        return self.name

    def getOrAddTag(self, tag: DataTypeTag):
        """
            Searches through the known tags of the field in order to find one with de desired DataType. 
            If not found, it adds it and returns the added object
        """
        fieldTagsWithTheDesiredDataTypeTag = list(
            filter(lambda fieldTag: fieldTag.tag.id == tag.id, self.tags)
        )

        if len(fieldTagsWithTheDesiredDataTypeTag) == 0:
            # Creates a new FieldTag and links it to self thus it is not necessary to call self.tags.append(newFieldTag)
            newFieldTag = FieldTag(self, tag, 0)

            return newFieldTag
        else:
            return fieldTagsWithTheDesiredDataTypeTag[0]

    def updateTag(self, tag: DataTypeTag, score: int) -> None:
        fieldTag = self.getOrAddTag(tag)
        fieldTag.certanty_score += score


    def run(self, controls: list['Control']):
        for control in controls:
            control.executeOn(self)

    def getDataSampleWithoutNones(self):
        return [dataPoint for dataPoint in self.dataSample if dataPoint is not None]