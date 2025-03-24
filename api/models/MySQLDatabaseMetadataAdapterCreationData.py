from pydantic import BaseModel, Field

class MySQLDatabaseMetadataAdapterCreationData(BaseModel):
    host: str = Field()
    port: int = Field(gt=-1, lt=65536)
    username: str = Field()
    password: str = Field()
