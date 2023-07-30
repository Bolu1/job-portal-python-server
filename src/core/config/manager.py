from functools import lru_cache

import decouple

from src.core.config.settings.base import BackendBaseSettings
from src.core.config.settings.development import BackendDevSettings
from src.core.config.settings.environment import Environment


class BackendSettingsFactory:
    def __init__(self, environment: str):
        self.environment = environment
        
    def __call__(self) -> BackendBaseSettings:
        return BackendDevSettings()
        
    
@lru_cache()
def get_settings()-> BackendBaseSettings:
    return BackendSettingsFactory(environment=decouple.config("ENVIRONMENT", default="DEV", cast=str))() # type: ignore

settings: BackendBaseSettings = get_settings()