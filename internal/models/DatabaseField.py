from internal.models.FieldDataTypes import FieldDataTypes
from internal.models.ControlTag import ControlTag

class DatabaseField():
    def __init__(self, name: str, type: FieldDataTypes):
        self.name = name
        self.type = FieldDataTypes
        self.dataSample = []

    def getName(self) -> str:
        return self.name
    
    def updateTags(self, tags: dict[ControlTag, int]) -> None:
        # TODO: Implement
        pass