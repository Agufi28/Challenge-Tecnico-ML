from abc import ABC, abstractmethod

from internal.models.DatabaseField import DatabaseField

class Control(ABC):
    def __init__(self, name: str):
        self.name = name

    @abstractmethod
    def executeOn(self, field: DatabaseField):
        pass