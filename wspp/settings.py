import enum
import tomllib
from pathlib import Path
from typing import Any

from pydantic import BaseModel, DirectoryPath, Field, PositiveInt
from pydantic.fields import FieldInfo
from pydantic_settings import (
    BaseSettings,
    EnvSettingsSource,
    PydanticBaseSettingsSource,
)
from typing_extensions import Annotated

from wspp import slack


class WsppSettings(BaseModel):
    latitude: Annotated[float, Field(ge=-90.0, le=90.0)]
    longitude: Annotated[float, Field(ge=-180.0, le=180.0)]
    profile_photos_dir: DirectoryPath = Path(__file__).parent.parent / "profile_photos"
    polling_interval_s: PositiveInt = 7200


class ProviderName(enum.Enum):
    WEATHERSTACK = "weatherstack"
    WEATHERAPI = "weatherapi"


class WeatherproviderSettings(BaseModel):
    name: ProviderName
    api_access_key: str


# https://github.com/pydantic/pydantic/issues/2335
class TOMLConfigSettingsSource(PydanticBaseSettingsSource):
    def get_field_value(
        self, field: FieldInfo, field_name: str
    ) -> tuple[Any, str, bool]:
        return super().get_field_value(field, field_name)

    def __call__(self) -> dict[str, Any]:
        return tomllib.loads(Path("config.toml").read_text())


class Settings(BaseSettings):
    wspp: WsppSettings
    weatherprovider: WeatherproviderSettings
    slack: list[slack.SlackSettings]

    @classmethod
    def settings_customise_sources(
        cls, *_args, **_kwargs
    ) -> tuple[PydanticBaseSettingsSource, ...]:
        return (
            EnvSettingsSource(Settings, env_nested_delimiter="__"),
            TOMLConfigSettingsSource(Settings),
        )


settings = Settings()
