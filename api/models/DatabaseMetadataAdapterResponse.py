from pydantic import BaseModel, Field

class DatabaseMetadataAdapterResponse(BaseModel):
    id: int = Field()
    type: str = Field()
