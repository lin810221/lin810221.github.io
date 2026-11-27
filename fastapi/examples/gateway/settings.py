from pathlib import Path
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix='RELAY_', extra='ignore')
    database_path: Path = Path('.runtime/relay.sqlite3')
    max_body_bytes: int = Field(default=16_384, ge=1024, le=1_048_576)
    stream_seconds: float = Field(default=10, gt=0, le=60)
    allowed_origins: list[str] = ['http://localhost:3000']
    allowed_hosts: list[str] = ['localhost', '127.0.0.1', 'testserver']

    def public(self):
        return {'database': self.database_path.name, 'max_body_bytes': self.max_body_bytes}
