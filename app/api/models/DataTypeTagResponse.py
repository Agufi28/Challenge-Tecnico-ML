from pydantic import BaseModel, Field

class DataTypeTagResponse(BaseModel):
    id: int = Field()
    name: str = Field()
    description: str | None = Field()

