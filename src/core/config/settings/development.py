from src.core.config.settings.environment import Environment
from src.core.config.settings.base import BackendBaseSettings

class BackendDevSettings(BackendBaseSettings):
    DESCRIPTION: str | None = "Development Environment."
    DEBUG: bool = True
    ENVIRONMENT: Environment = Environment.DEVELOPMENT
