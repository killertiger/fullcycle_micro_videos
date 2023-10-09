from typing import Dict, Optional
import os
from pathlib import Path
import dj_database_url
from pydantic import validator, Field
from pydantic_settings import BaseSettings

_ENV_FOLDER = Path(__file__).resolve().parent.parent.parent / 'envs'

APP_ENV = os.getenv('APP_ENV')

class ConfigService(BaseSettings):
    database_dsn: str
    database_conn: Dict | None = Field(init=False, default=None)
    debug: bool = False
    language_code: str = 'en-us'
    secret_key: str
    
    class Config:
        env_file = f'{_ENV_FOLDER}/.env', f'{_ENV_FOLDER}/.env.{APP_ENV}'
        
    @validator('database_conn', pre=True, allow_reuse=True)
    def make_database_conn(cls, v, values, **kwargs):
        return dj_database_url.config(default=values['database_dsn'])
        
config_service = ConfigService()

