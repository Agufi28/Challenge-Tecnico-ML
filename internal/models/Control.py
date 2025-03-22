from abc import ABC, abstractmethod

from internal.models.DatabaseField import DatabaseField
from internal.models.ControlTag import ControlTag

class Control(ABC):
    """
        This class is a generalization of the controls that can be applied on the DatabaseField in order to classify them on the different categories.

        :param name: name of the control
        :param affectedTags: dictionary of the taggs that should be added to the field with their corresponding certanty score. If the tag LAST_NAME should get a 10 points boost when the control match; the dictionary should contain an entry with the tag as key and 10 as value
    """
    def __init__(self, name: str, affectedTags: dict[ControlTag, int]):
        self.name = name
        self.affectedTags = affectedTags

    @abstractmethod
    def __conditionMatches(self, field: DatabaseField) -> bool:
        pass

    def executeOn(self, field: DatabaseField):
        if self.__conditionMatches(field):
            field.updateTags(self.affectedTags)