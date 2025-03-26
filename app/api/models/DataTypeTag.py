from pydantic import BaseModel, Field

class DataTypeTagCreationData(BaseModel):
    name: str = Field()
    description: str | None = Field()

class DataTypeTagResponse(BaseModel):
    id: int = Field()
    name: str = Field()
    description: str | None = Field()

