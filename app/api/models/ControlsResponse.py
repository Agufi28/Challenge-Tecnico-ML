from typing import Any
from pydantic import BaseModel, Field

class ControlsResponse(BaseModel):
    id: int = Field()
    name: str = Field()
    type: str = Field()
    raw_data: str = Field()