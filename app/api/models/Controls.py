from typing import Any
from sqlalchemy import select
from pydantic import BaseModel, Field

from internal.models.DataTypeTag import DataTypeTag


class ControlsResponse(BaseModel):
    id: int = Field()
    name: str = Field()
    type: str = Field()
    raw_data: str = Field()

class ControlCreationData(BaseModel):
    name: str = Field()
    affectedTags: dict[str, int] = Field()
    def parsedAffectedTags(self, db) -> dict[DataTypeTag, int]:
        parsedTags: dict[DataTypeTag, int] = {}
        for tagName, score in self.affectedTags.items():
            tag = db.scalars(
                select(DataTypeTag)
                .where(DataTypeTag.name == tagName)
            ).first()
            
            if tag is None:
                raise ValueError("The provided tag name does not exist")
            
            parsedTags[tag] = score
        return parsedTags

class RegExOnFieldNameControlCreationData(ControlCreationData):
    regex: str = Field()

class RegExOnSampledDataControlCreationData(ControlCreationData):
    regex: str = Field()
