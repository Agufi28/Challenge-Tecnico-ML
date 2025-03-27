from datetime import datetime
import json
from typing import Any, Optional
from sqlalchemy import ForeignKey, String
from sqlalchemy import Text
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from internal.models.Base import Base
from internal.models.DatabaseField import DatabaseField
from internal.models.ControlAffectedTag import ControlAffectedTag
from internal.models.DataTypeTag import DataTypeTag
from internal.models.User import User

class Control(Base):
    __tablename__ = "controls"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    type: Mapped[str] = mapped_column(String(255))
    name: Mapped[str] = mapped_column(String(255))
    created_by_id: Mapped[Optional[int]] = mapped_column(ForeignKey("users.id"))
    createdBy: Mapped[Optional[User]] = relationship()
    created_at: Mapped[datetime] = mapped_column(default=datetime.now())
    # The size of this column is arbitrarly defined. 
    # The idea behind it is to store the required data to perform the control in any stringified format. 
    # Each control type will be responsable for knwoing how to parse it appropietly for reading and storing. 
    # e.g. if a control checks if the value is contained on a list, 
    # the data may be a strigified json array and the control implementation would be responsable for parsing it back to an array when needed
    raw_data: Mapped[str] = mapped_column(Text()) 
    affectedTags: Mapped[list[ControlAffectedTag]] = relationship(back_populates='control')

    __mapper_args__ = {
        "polymorphic_on": "type",
    }

    """
        This class is a generalization of the controls that can be applied on the DatabaseField in order to classify them on the different categories.

        :param name: name of the control
        :param affectedTags: dictionary of the taggs that should be added to the field with their corresponding certanty score. If the tag LAST_NAME should get a 10 points boost when the control match; the dictionary should contain an entry with the tag as key and 10 as value
    """
    def __init__(self, name: str, affectedTags: dict[DataTypeTag, int], createdBy: User = None, data: dict[str, Any]={}):
        self.name = name
        self.createdBy = createdBy
        self.raw_data = json.dumps(data)
        for tag, affectedScore in affectedTags.items():
            self.affectedTags.append(ControlAffectedTag(self, tag, affectedScore))

    def __conditionMatches(self, field: DatabaseField) -> bool:
        raise Exception("Must be implemented!")

    def getData(self) -> dict[str, Any]:
        return json.loads(self.raw_data)

    def executeOn(self, field: DatabaseField):
        if self.__conditionMatches(field):
            for affectedTag in self.affectedTags:
                field.updateTag(affectedTag.tag, affectedTag.affect_score_by)