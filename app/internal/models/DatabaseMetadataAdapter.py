from typing import Optional
from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from internal.errors.ScanException import ScanException
from internal.models.Base import Base
from internal.models.Control import Control
from internal.models.ScanResult import ScanResult
from internal.models.DatabaseSchema import DatabaseSchema

class DatabaseMetadataAdapter(Base):
    __tablename__ = "databases"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    type: Mapped[str] = mapped_column(String(10))

    __mapper_args__ = {
        "polymorphic_on": "type",
    }

    scans: Mapped[list[ScanResult]] = relationship(cascade="all, delete-orphan", back_populates='database')


    """
        Must be implemented! 
        
        This method should handle the connection to the database using the correspondig driver, 
        fetch the structure, parse it and return a list of DatabaseSchema objects. 

        The idea behind this architecture is to allow an easy support for different database types. 
        The only neccesary change would be adding a new child of this class with the corresponding implementation. 

        :param dataSampleSize: Set to any n positive integer in order to get a random sample of up to n values of the column. Note: If the column contains less than n values, all the values will be fetched.
    """
    def scanStructure(self, dataSampleSize=0) -> ScanResult:
        raise Exception("Must be implemented!")

    def fetchSamples(self,  dataSampleSize, structure:list[DatabaseSchema], cursor):
        raise Exception("Must be implemented!")

    def getLastScan(self):
        if len(self.scans) == 0:
            raise ScanException("The database has not been scanned yet")
        return self.scans[-1]
    
    """
        Runs the received controls on the last scanned structure of the database.
    """
    def runControlsOnLastScan(self, controls: list[Control]):
        self.getLastScan().run(controls)