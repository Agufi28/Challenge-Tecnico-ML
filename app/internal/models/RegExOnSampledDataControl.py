import json
import re

from internal.models.Control import Control
from internal.models.DataTypeTag import DataTypeTag
from internal.models.User import User
from internal.models.DatabaseField import DatabaseField
from internal.models.FieldDataTypes import FieldDataTypes

class RegExOnSampledDataControl(Control):
    __mapper_args__ = {
        "polymorphic_identity": "RegExOnSampledData",
    }

    """
        This is a type of control based on the field data ata sampled from de database. Requires a regular expression to match the data.

        :param name: user friendly name for the control
        :param affectedTags: dictionary of the taggs that should be added to the field with their corresponding certanty score. If the tag LAST_NAME should get a 10 points boost when the control match; the dictionary should contain an entry with the tag as key and 10 as value
        :param regex: Regular expression used 
    """
    def __init__(self, name: str, affectedTags: dict[DataTypeTag, int], regex :str, createdBy: User = None):
        super().__init__(name, affectedTags, createdBy)
        self.raw_data = json.dumps({'regex': regex})

    # This is the implementation of the get data for the regex scenario. No special parsing is needed since the regex is an string and the raw_data is too
    def getData(self):
        return json.loads(self.raw_data)

    # This method only exists to provide aditional semantics and allow for extra values to be stored on the data
    def getRegEx(self):
        return self.getData()['regex']

    # This is the implementation for the abstract private method __conditionMatches of the parent class Control
    def _Control__conditionMatches(self, field: DatabaseField):
        # This control type can only run on STRING datasamples 
        if field.type != FieldDataTypes.STRING:
            return False
        # The condition matches if the regex finds any conincidence on the field data samples
        return any(map(lambda samplePoint: re.search(self.getRegEx(), str(samplePoint)) is not None, field.getDataSampleWithoutNones()))