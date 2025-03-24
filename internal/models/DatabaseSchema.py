from sqlalchemy import String
from sqlalchemy import ForeignKey

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from internal.models.Base import Base
from internal.models.DatabaseTable import DatabaseTable


class DatabaseSchema(Base):
    __tablename__ = "schemas"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(64), nullable=False)
    tables: Mapped[list[DatabaseTable]] = relationship(back_populates="schema")

    database_id: Mapped[int] = mapped_column(ForeignKey("databases.id"))
    database = relationship("DatabaseMetadataAdapter", back_populates="schemas")

    def __init__(self, name, tables=None):
        self.name = name

        if tables is not None:
            self.tables = tables
        else:
            self.tables = []
    
    def addTable(self, table):
        self.tables.append(table)

    def getName(self):
        return self.name
    
    def getTables(self):
        return self.tables
    
    def getLastTable(self):
        if(len(self.tables) == 0):
            return None
        else:
            return self.tables[-1]
        
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