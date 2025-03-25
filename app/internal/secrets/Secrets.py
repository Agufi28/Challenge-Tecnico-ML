import os
from dotenv import load_dotenv
from internal.errors.SecretsException import SecretsException
from loguru import logger

load_dotenv()
"""
    This class acts as a proxy to abstract the fetching process of sensitive information 
    and allows for an easy modification of this mechanisms withot suffering the gunshot surgery smell.
"""
class Secrets():
    def __getEnvOrFail(env, secretName):
        data = os.getenv(env)
        if data is None:
            logger.error(f"Missing environment variable [{env}]")
            raise SecretsException(f"Error fetching the {secretName} secret")
        return data
    
    def getDatabaseEncryptionKey():
        return Secrets.__getEnvOrFail("DATABASE_ENCRYPTION_KEY", "databaseEncryptionKey")

    def getDatabaseUser():
        return Secrets.__getEnvOrFail("DATABASE_USER", "databaseUser")

    def getDatabasePassword():
        return Secrets.__getEnvOrFail("DATABASE_PASSWORD", "databasePassword")

    def getDatabaseHost():
        return Secrets.__getEnvOrFail("DATABASE_HOST", "databaseHost")

    def getDatabasePort():
        return Secrets.__getEnvOrFail("DATABASE_PORT", "databasePort")
        
    def getDatabaseName():
        return Secrets.__getEnvOrFail("DATABASE_NAME", "databaseName")
