from pydantic import BaseModel, Field

class UserCreationData(BaseModel):
    username: str = Field()
    password: str = Field()
    is_admin: bool = Field

class UserData(BaseModel):
    id: int = Field()
    username: str = Field()
    is_admin: bool = Field()