from pathlib import Path

import tomllib
from pydantic import BaseModel, BaseSettings, DirectoryPath, PositiveInt
from pydantic.env_settings import EnvSettingsSource
from pydantic.utils import deep_update

from wspp import slack, weatherstack


class WsppSettings(BaseModel):
    latitude: float
    longitude: float
    profile_photos_dir: DirectoryPath = Path(__file__).parent.parent / "profile_photos"
    polling_interval_s: PositiveInt = 7200


class Settings(BaseSettings):
    wspp: WsppSettings
    weatherstack: weatherstack.WeatherstackSettings
    slack: slack.SlackSettings

    @classmethod
    def read(cls):
        # Pydantic doesn't have built-in support for toml files, so we
        # have to load the toml file (and override with any env vars)
        # ourselves.
        # https://github.com/pydantic/pydantic/issues/2335
        toml_settings = Settings(**tomllib.loads(Path("config.toml").read_text()))
        env_data = EnvSettingsSource(
            env_file=None,
            env_file_encoding=None,
            env_nested_delimiter="__",
        )(toml_settings)
        return Settings.parse_obj(obj=deep_update(toml_settings.dict(), env_data))


settings = Settings.read()
