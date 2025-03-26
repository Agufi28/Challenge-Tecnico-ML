from pydantic import BaseModel, Field

class ScanDatabaseResponse(BaseModel):
    id: int = Field()