from pydantic import BaseModel, Field

from sqlalchemy import select

from internal.models.DataTypeTag import DataTypeTag

class RegExOnFieldNameControlCreationData(BaseModel):
    name: str = Field()
    regex: str = Field()
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
