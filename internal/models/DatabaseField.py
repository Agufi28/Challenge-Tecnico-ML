from internal.models.FieldDataTypes import FieldDataTypes

class DatabaseField():
    def __init__(self, name: str, type: FieldDataTypes):
        self.name = name
        self.type = FieldDataTypes
        self.dataSample = []