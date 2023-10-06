from typing import Dict
from pydantic_settings import BaseSettings

class ConfigService(BaseSettings):
    database_dsn: str
    database_conn: Dict = None
    debug: bool = False
    language_code: str = 'en-us'
    secret_key: str