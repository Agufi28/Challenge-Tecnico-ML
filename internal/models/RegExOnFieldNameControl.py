import re

from internal.models.Control import Control
from internal.models.ControlTag import ControlTag

class RegExOnFieldNameControl(Control):
    """
        This is a type of control based on the name of the field. Requires a regular expression to match the field to.

        :param name: user friendly name for the control
        :param affectedTags: dictionary of the taggs that should be added to the field with their corresponding certanty score. If the tag LAST_NAME should get a 10 points boost when the control match; the dictionary should contain an entry with the tag as key and 10 as value
        :param regex: Regular expression used 
    """
    def __init__(self, name: str, affectedTags: dict[ControlTag, int], regex :str):
        super().__init__(name, affectedTags)
        self.regex = regex

    # This is the implementation for the abstract private method __conditionMatches of the parent class Control
    def _Control__conditionMatches(self, field):
        # The condition matches if the regex finds any conincidence on the field name
        return re.search(self.regex, field.getName()) is not None