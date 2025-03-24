from sqlalchemy import String
from sqlalchemy import ForeignKey

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from internal.models.Base import Base
from internal.models.DatabaseTable import DatabaseTable
from internal.models.Control import Control

class DatabaseSchema(Base):
    __tablename__ = "schemas"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(64), nullable=False)
    tables: Mapped[list[DatabaseTable]] = relationship(cascade="all, delete-orphan")

    database_id: Mapped[int] = mapped_column(ForeignKey("databases.id"))

    def __init__(self, name, tables=None):
        self.name = name

        if tables is not None:
            self.tables = tables
        else:
            self.tables = []
    
    def getName(self) -> str:
        return self.name

    def addTable(self, table) -> None:
        self.tables.append(table)

    def getTables(self):
        return self.tables

    def getOrAddTable(self, name):
        """
            Searches through the known tables of the schema in order to find a table with the desired name. 
            If not found, it adds it and returns the added object
        """
        tablesWithTheDesiredName = list(filter(lambda table: table.getName() == name, self.tables))

        if len(tablesWithTheDesiredName) == 0:
            newTable = DatabaseTable(name)
            self.addTable(newTable)

            return newTable
        else:
            return tablesWithTheDesiredName[0]

    def run(self, controls: list[Control]):
        for table in self.getTables():
            table.run(controls)