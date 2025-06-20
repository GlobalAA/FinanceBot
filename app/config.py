from pathlib import Path

from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

ROOT_DIR = Path(__file__).parent.parent

class Config(BaseSettings):
	BOT_TOKEN: SecretStr
	DB_URL: SecretStr

	model_config = SettingsConfigDict(
		env_file=ROOT_DIR / ".env",
		env_file_encoding='utf-8'
	)

config = Config()