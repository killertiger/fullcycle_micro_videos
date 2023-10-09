from typing import Dict, Optional, List
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
    installed_apps: List[str]
    language_code: str = 'en-us'
    secret_key: str

    
    class Config:
        env_file = f'{_ENV_FOLDER}/.env', f'{_ENV_FOLDER}/.env.{APP_ENV}'
        
        # @classmethod - should use https://docs.pydantic.dev/2.0/migration/ customise settings sources
        # def parse_env_var(cls, field_name: str, raw_value):
        #     if field_name == 'installed_apps':
        #         return [item.strip() for item in raw_value.splitlines() if item.strip() != '']
        #     return cls.json_loads(raw_value)
        
    
        
    @validator('database_conn', pre=True, allow_reuse=True)
    def make_database_conn(cls, v, values, **kwargs):
        return dj_database_url.config(default=values['database_dsn'])
        
config_service = ConfigService()

