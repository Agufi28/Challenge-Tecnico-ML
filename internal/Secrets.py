import os
from dotenv import load_dotenv

load_dotenv()
"""
    This class acts as a proxy to abstract the fetching process of sensitive information 
    and allows for an easy modification of this mechanisms withot suffering the gunshot surgery smell.
"""
class Secrets():
    def getDatabaseEncryptionKey():
        return os.getenv("DATABASE_ENCRYPTION_KEY")