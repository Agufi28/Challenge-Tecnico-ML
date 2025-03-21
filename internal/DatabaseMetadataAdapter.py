from abc import ABC, abstractmethod

class DatabaseMetadataAdapter(ABC):

    """
        Must be implemented! 
        
        This method should handle the connection to the database using the correspondig driver, 
        fetch the structure, parse it and return a list of DatabaseTable objects. 

        The idea behind this architecture is to allow an easy support for different database types. 
        The only neccesary change would be adding a new child of this class with the corresponding implementation. 

        :param dataSampleSize: Set to any n positive integer in order to get a random sample of up to n values of the column. Note: If the column contains less than n values, all the values will be fetched.
    """
    @abstractmethod
    def getStructure(self, dataSampleSize=0):
        pass
