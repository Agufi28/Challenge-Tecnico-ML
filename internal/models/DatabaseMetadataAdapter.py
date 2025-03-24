from sqlalchemy import String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from internal.models.Base import Base
from internal.models.DatabaseSchema import DatabaseSchema

class DatabaseMetadataAdapter(Base):
    __tablename__ = "databases"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    type: Mapped[str] = mapped_column(String(10))

    __mapper_args__ = {
        "polymorphic_on": "type",
    }

    schemas: Mapped[list[DatabaseSchema]] = relationship(cascade="all, delete-orphan")

    """
        Must be implemented! 
        
        This method should handle the connection to the database using the correspondig driver, 
        fetch the structure, parse it and return a list of DatabaseSchema objects. 

        The idea behind this architecture is to allow an easy support for different database types. 
        The only neccesary change would be adding a new child of this class with the corresponding implementation. 

        :param dataSampleSize: Set to any n positive integer in order to get a random sample of up to n values of the column. Note: If the column contains less than n values, all the values will be fetched.
    """
    
    def updateStructure(self) -> None:
        raise Exception("Must be implemented!")

    def fetchSamples(self, dataSampleSize=0):
        raise Exception("Must be implemented!")

    def getStructure(self,  dataSampleSize=0)-> list[DatabaseSchema]:
        self.updateStructure()
        if dataSampleSize != 0:
            self.fetchSamples()
        return self.schemas