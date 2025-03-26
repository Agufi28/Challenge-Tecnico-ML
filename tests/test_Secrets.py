from unittest.mock import patch
import pytest
from internal.secrets.Secrets import Secrets, SecretsException


class TestSecrets():
    @patch("os.getenv", return_value="test_key")
    def test_getDatabaseEncryptionKey_with_env_var(self, getenv):
        result = Secrets.getDatabaseEncryptionKey()
        assert result == "test_key"
    
    @patch("os.getenv", return_value=None)
    def test_getDatabaseEncryptionKey_without_env_var(self, getenv):
        with pytest.raises(SecretsException) as exc_info:
            Secrets.getDatabaseEncryptionKey()

    @patch("os.getenv", return_value=None)
    def test__Secrets__getEnvOrFail_without_env_var(self, getenv):
        with pytest.raises(SecretsException):
            Secrets._Secrets__getEnvOrFail("DATABASE_ENCRYPTION_KEY", "databaseEncryptionKey")

    @patch("os.getenv", return_value="test_key")
    def test_getEnvOrFail_with_env_var(self, getenv):
        result = Secrets._Secrets__getEnvOrFail("DATABASE_ENCRYPTION_KEY", "databaseEncryptionKey")
        assert result == "test_key"