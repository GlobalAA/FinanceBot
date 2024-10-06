from os import path

from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
	BOT_TOKEN: SecretStr

	model_config = SettingsConfigDict(
		env_file=path.join(path.dirname(__file__), ".env"),
		env_file_encoding="utf-8",
	)

config = Config()