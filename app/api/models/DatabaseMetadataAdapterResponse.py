from pydantic import BaseModel, Field
from api.models.UserCreation import UserData
class DatabaseMetadataAdapterResponse(BaseModel):
    id: int = Field()
    type: str = Field()
    createdBy: UserData | None = Field
