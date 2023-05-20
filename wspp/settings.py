from pathlib import Path

from pydantic import BaseSettings, DirectoryPath, PositiveInt

from wspp import slack, weatherstack


class Settings(BaseSettings):
    weatherstack: weatherstack.WeatherstackSettings
    slack: slack.SlackSettings
    latitude: float
    longitude: float
    profile_photos_dir: DirectoryPath = Path(__file__).parent.parent / "profile_photos"
    polling_interval_s: PositiveInt = 7200

    class Config:
        env_file = ".env"
        env_nested_delimiter = "__"


settings = Settings()
