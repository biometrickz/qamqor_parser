from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class EnvironmentSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file='../.env', env_file_encoding='utf-8')

    mongo_host: str = Field('MONGO_HOST')
    mongo_port: int = Field('MONGO_PORT')
    mongo_db: str = Field('MONGO_DB')


settings = EnvironmentSettings()
