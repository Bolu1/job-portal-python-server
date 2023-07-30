import logging
import decouple
import pydantic
import pathlib

from pydantic_settings import BaseSettings

ROOT_DIR: pathlib.Path = pathlib.Path(__file__).parent.parent.parent.parent.parent.resolve()

 
class BackendBaseSettings(BaseSettings):
    PROJECT_NAME:str = "Trabajo"
    PROJECT_VERSION: str = "1.0.0"
    DEBUG: bool = False
    API_PREFIX: str = "/api"
    DOCS_URL: str = "/docs"
    OPENAPI_URL: str = "/openapi.json"
    REDOC_URL: str = "/redoc"
    OPENAPI_PREFIX: str = ""
    
    #Server Details
    SERVER_HOST: str = decouple.config("BACKEND_SERVER_HOST", cast=str)  # type: ignore
    SERVER_PORT: int = decouple.config("BACKEND_SERVER_PORT", cast=int)  # type: ignore
    SERVER_WORKERS: int = decouple.config("BACKEND_SERVER_WORKERS", cast=int)  # type: ignore

    # DB Details
    POSTGRES_USER : str = decouple.config("POSTGRES_USER", cast=str)
    POSTGRES_PASSWORD: str = decouple.config("POSTGRES_PASSWORD", cast=str)
    POSTGRES_HOST : str = decouple.config("POSTGRES_HOST","localhost", cast=str)
    POSTGRES_PORT : int = decouple.config("POSTGRES_PORT",5432, cast=int) 
    POSTGRES_SCHEMA: str = decouple.config("POSTGRES_SCHEMA", cast=str) 
    POSTGRES_DB : str = decouple.config("POSTGRES_DB","tdd", cast=str)
    DATABASE_URL: str = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
    DB_POOL_SIZE: int = decouple.config("DB_POOL_SIZE", cast=int)  # type: ignore
    DB_POOL_OVERFLOW: int = decouple.config("DB_POOL_OVERFLOW", cast=int)  # type: ignore
    
    # DB Driver Details
    IS_DB_ECHO_LOG: bool = decouple.config("IS_DB_ECHO_LOG", cast=bool)  # type: ignore
    
    
    # JWT Details
    JWT_TOKEN_PREFIX: str = decouple.config("JWT_TOKEN_PREFIX", cast=str) 
    JWT_SECRET_KEY: str = decouple.config("JWT_SECRET_KEY", cast=str) 
    JWT_SUBJECT: str = decouple.config("JWT_SUBJECT", cast=str) 
    JWT_MIN: int = decouple.config("JWT_MIN", cast=int) 
    JWT_HOUR: int = decouple.config("JWT_HOUR", cast=int) 
    JWT_DAY: int = decouple.config("JWT_DAY", cast=int) 
    JWT_ACCESS_TOKEN_EXPIRATION_TIME: int = JWT_MIN * JWT_HOUR * JWT_DAY
    
    #CORS Details
    IS_ALLOWED_CREDENTIALS: bool = decouple.config("IS_ALLOWED_CREDENTIALS", cast=bool)  # type: ignore
    ALLOWED_ORIGINS: list[str] = [
        "http://localhost:3000",
        "http://localhost:5173",
    ]
    ALLOWED_METHODS: list[str] = ["*"]  #all methods
    ALLOWED_HEADERS: list[str] = ["*"]  #all methods
    
    # Logging Details
    LOGGING_LEVEL: int = logging.INFO
    LOGGERS: tuple[str, str] = ("uvicorn.asgi", "uvicorn.access")
    
    #Hashing Details
    HASHING_ALGORITHM_LAYER_1: str = decouple.config("HASHING_ALGORITHM_LAYER_1", cast=str)  # type: ignore
    HASHING_ALGORITHM_LAYER_2: str = decouple.config("HASHING_ALGORITHM_LAYER_2", cast=str)  # type: ignore
    HASHING_SALT: str = decouple.config("HASHING_SALT", cast=str)  # type: ignore
    JWT_ALGORITHM: str = decouple.config("JWT_ALGORITHM", cast=str)  # type: ignore
    
    class Config(pydantic.BaseConfig):
        case_sensitive: bool = True
        env_file: str = f"{str(ROOT_DIR)}/.env"
        validate_assignment: bool = True

    @property
    def set_backend_app_attributes(self) -> dict[str, str | bool | None]:
        return {
            "title": self.PROJECT_NAME,
            "version": self.PROJECT_VERSION,
            "debug": self.DEBUG,
            "description": self.DESCRIPTION,
            "docs_url": self.DOCS_URL,
            "openapi_url": self.OPENAPI_URL,
            "redoc_url": self.REDOC_URL,
            "openapi_prefix": self.OPENAPI_PREFIX,
            "api_prefix": self.API_PREFIX,
        }
