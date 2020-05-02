import logging
import os

CONFIG_EXPECTED_KEYS = ["SQLALCHEMY_DATABASE_URI"]
# use local "TEMPLATE" DB for local dev
DEFAULT_DB_URL = "postgresql:///ocp"


class Config:
    """Base config."""

    SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI", DEFAULT_DB_URL)
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # set SQL_ECHO=1 this to echo queries to stderr
    SQLALCHEMY_ECHO = bool(os.getenv("SQL_ECHO"))
    DEBUG = os.getenv("DEBUG", False)
    TESTING = bool(os.getenv("TESTING"))

    NPLUSONE_LOGGER = logging.getLogger("app.nplusone")
    NPLUSONE_LOG_LEVEL = logging.WARNING

    DEBUG = True
    DEV_DB_SCRIPTS_ENABLED = True


# config checks


class ConfigurationInvalidError(Exception):
    def __init__(self, message: str):
        self.message = message

    def __str__(self):
        return self.message


class ConfigurationKeyMissingError(ConfigurationInvalidError):
    def __init__(self, key: str):
        super().__init__(message=f"Missing {key} key in configuration.")


class ConfigurationValueMissingError(ConfigurationInvalidError):
    def __init__(self, key: str):
        super().__init__(message=f"Missing {key} value in configuration.")


def check_valid(conf) -> bool:
    """Check if config looks okay."""

    def need_key(k):
        if k not in conf:
            raise ConfigurationKeyMissingError(k)

        if not conf.get(k):
            raise ConfigurationValueMissingError(k)

    [need_key(k) for k in CONFIG_EXPECTED_KEYS]
    return True
