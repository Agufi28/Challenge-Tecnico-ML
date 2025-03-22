import pymysql.cursors

from loguru import logger

from internal.DatabaseMetadataAdapter import DatabaseMetadataAdapter
from internal.models.DatabaseSchema import DatabaseSchema
from internal.models.DatabaseTable import DatabaseTable
from internal.models.DatabaseField import DatabaseField
from internal.models.FieldDataTypes import FieldDataTypes



class MySQLDatabaseMetadataAdapter(DatabaseMetadataAdapter):
    # Nota para quien corrija esto: Si bien se que esta solución a priori parecería dificil de mantener, surge de una evaluación costo beneficio.
    # Estandarizar los tipos de dato me permite estandarizar las verificaciones, de forma que un control aplica a cualquier base de datos, sin cuál sea. 
    # Y, consideré que la probabilidad de que el sistema deba contemplar un tipo de base de datos nueva, como SQL Server o PostgreSQL es mucho mayor a la probabilidad de que un motor de base de datos bien establecido agregue tipos de dato nuevos.
    # Debido a esto, elegí tener extensibilidad en los motores de base de datos a soportar en pos del costo en desarrollos adaptativos adicionales.

    mysqlTypesToStandarTypes = {
        'varchar': FieldDataTypes.STRING,
        'char': FieldDataTypes.STRING,
        'text': FieldDataTypes.STRING,
        'tinytext': FieldDataTypes.STRING,
        'mediumtext': FieldDataTypes.STRING,
        'longtext': FieldDataTypes.STRING,
        'set': FieldDataTypes.STRING,
        'enum': FieldDataTypes.STRING,
        'blob': FieldDataTypes.STRING,
        'tinyblob': FieldDataTypes.STRING,
        'mediumblob': FieldDataTypes.STRING,
        'longblob': FieldDataTypes.STRING,
        'binary': FieldDataTypes.STRING,
        'varbinary': FieldDataTypes.STRING,
        'int': FieldDataTypes.INTEGER,
        'tinyint': FieldDataTypes.INTEGER,
        'mediumint': FieldDataTypes.INTEGER,
        'bigint': FieldDataTypes.INTEGER,
        'bit': FieldDataTypes.INTEGER,
        'float': FieldDataTypes.DECIMAL,
        'double': FieldDataTypes.DECIMAL,
        'decimal': FieldDataTypes.DECIMAL,
        'date': FieldDataTypes.DATE,
        'time': FieldDataTypes.TIME,
        'datetime': FieldDataTypes.DATETIME,
        'timestamp': FieldDataTypes.DATETIME,
    }

    def __init__(self, host, port, username, password):
        self.host = host
        self.port = port
        self.username = username
        self.password = password

    def getStructure(self, dataSampleSize=0) -> list[DatabaseTable]:
        with pymysql.connect(
            host=self.host,
            port=self.port,
            user=self.username,
            password=self.password,
            cursorclass=pymysql.cursors.DictCursor
        ) as connection:
            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT 
                        t.TABLE_SCHEMA,
                        t.TABLE_NAME,
                        c.COLUMN_NAME,
                        c.DATA_TYPE
                    FROM INFORMATION_SCHEMA.TABLES as t
                    
                    INNER JOIN INFORMATION_SCHEMA.COLUMNS as c ON c.TABLE_SCHEMA = t.TABLE_SCHEMA AND c.TABLE_NAME = t.TABLE_NAME
                    WHERE t.TABLE_TYPE = 'BASE TABLE' 
                        AND t.ENGINE = 'InnoDB' 
                        AND t.TABLE_SCHEMA != 'mysql'
                    ORDER BY t.TABLE_SCHEMA, t.TABLE_NAME
                """)

                # By the end of this method, this list will contain all the found schemas and thir corresponding columns and fields
                schemas = []

                data = cursor.fetchone()
                while data is not None:
                    # This loop actually contains three nested control breaks, thus only the fist one is evident. 
                    # The other two are contained within the used class methods.
                    if len(schemas) == 0 or schemas[-1].getName() != data["TABLE_SCHEMA"]:
                        schemas.append(DatabaseSchema(data["TABLE_SCHEMA"]))

                    currentSchema = schemas[-1]

                    currentSchema.getOrAddTable(data["TABLE_NAME"]).addField(
                        DatabaseField(
                            name=data["COLUMN_NAME"],
                            # The returned types are standarized with the objective of not having to know the actual database motor used.
                            type=MySQLDatabaseMetadataAdapter.mysqlTypesToStandarTypes[data["DATA_TYPE"]] 
                        )
                    )

                    data = cursor.fetchone()

                #TODO: Fetch the data samples.
                return schemas