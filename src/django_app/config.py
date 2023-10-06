from typing import Dict, Optional
import os
from pathlib import Path
from pydantic_settings import BaseSettings

_ENV_FOLDER = Path(__file__).resolve().parent.parent.parent / 'envs'

class ConfigService(BaseSettings):
    database_dsn: str
    database_conn: Dict | None = None
    debug: bool = False
    language_code: str = 'en-us'
    secret_key: str
    
    class Config:
        env_file = f'{_ENV_FOLDER}/.env'
        
config_service = ConfigService()