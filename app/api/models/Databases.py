from pydantic import BaseModel, Field
from app.api.models.Users import UserData

class DatabaseMetadataAdapterResponse(BaseModel):
    id: int = Field()
    type: str = Field()
    createdBy: UserData | None = Field

class MySQLDatabaseMetadataAdapterCreationData(BaseModel):
    host: str = Field()
    port: int = Field(gt=-1, lt=65536)
    username: str = Field()
    password: str = Field()
