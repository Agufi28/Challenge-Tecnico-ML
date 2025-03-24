import os
from dotenv import load_dotenv
from internal.secrets.SecretsException import SecretsException
from loguru import logger

load_dotenv()
"""
    This class acts as a proxy to abstract the fetching process of sensitive information 
    and allows for an easy modification of this mechanisms withot suffering the gunshot surgery smell.
"""
class Secrets():
    def getDatabaseEncryptionKey():
        return Secrets.__getEnvOrFail("DATABASE_ENCRYPTION_KEY", "databaseEncryptionKey")

    def __getEnvOrFail(env, secretName):
        data = os.getenv(env)
        if data is None:
            logger.error(f"Missing environment variable [{env}]")
            raise SecretsException(f"Error fetching the {secretName} secret")
        return data