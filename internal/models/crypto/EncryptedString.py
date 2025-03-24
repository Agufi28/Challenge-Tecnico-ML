from cryptography.fernet import Fernet
from sqlalchemy import Text
from sqlalchemy import TypeDecorator

class EncryptedString(TypeDecorator):
    impl = Text
    cache_ok = True

    def __init__(self, encryption_key: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.encryption_key = encryption_key
        self.fernet = Fernet(encryption_key.encode())

    def process_bind_param(self, value: str, dialect):
        if value is not None:
            value = self.fernet.encrypt(value.encode()).decode()
        return value

    def process_result_value(self, value:str, dialect):
        if value is not None:
            value = self.fernet.decrypt(value.encode()).decode()
        return value