class DatabaseTable():
    def __init__(self, name, fields=[]):
        self.name = name
        self.fields = fields

    def addField(self, field):
        self.fields.append(field)

    def getName(self):
        return self.name
    
    def getFields(self):
        return self.fields
    
    def getLastField(self):
        if(len(self.fields) == 0):
            return None
        else:
            return self.fields[-1]