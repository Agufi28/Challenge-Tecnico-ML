from sqlalchemy import String
from sqlalchemy import ForeignKey

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from internal.models.Base import Base
from internal.models.DatabaseField import DatabaseField
class DatabaseTable(Base):
    __tablename__ = "schema_tables"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(64), nullable=False)

    schema_id: Mapped[int] = mapped_column(ForeignKey("schemas.id"))
    # This attributtes are required in order to achieve a sound relational structure between the mappedclass objects
    schema = relationship("DatabaseSchema", back_populates="tables")
    fields: Mapped[list[DatabaseField]] = relationship(back_populates="table")

    def __init__(self, name, fields=None):
        self.name = name

        if fields is not None:
            self.fields = fields    
        else:
            self.fields = []

    def addField(self, field):
        self.fields.append(field)

    def getName(self):
        return self.name
    
    def getFields(self):
        return self.fields
    
    def getLastField(self):
        if(len(self.fields) == 0):
            return None
        else:
            return self.fields[-1]