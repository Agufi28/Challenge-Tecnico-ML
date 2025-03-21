from internal import DatabaseMetadataAdapter
import pymysql.cursors

class MySQLDatabaseMetadataAdapter(DatabaseMetadataAdapter):

    def __init__(self, host, port, username, password):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
    
    def __getConnection(self):
        return pymysql.connect(
            host=self.host,
            user=self.username,
            password=self.password,
            database=self.database,
            cursorclass=pymysql.cursors.DictCursor
        )
    
    def getStructure():
        #TODO: Implement
        pass