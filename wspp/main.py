"""
Script which periodically:
* fetches the weather condition of a specified location, 
* selects a background image based on the weather condition,
* creates a new profile photo using this background image and a provided profile photo,
* and updates the user's profile photo in Slack with this new profile photo.
"""

import dataclasses
import logging
from pathlib import Path
from threading import Event
from typing import Optional

from pydantic import BaseSettings, DirectoryPath, PositiveInt

from wspp import image, schedule, slack, weatherstack
from wspp.sunrisesunset import SunriseSunset


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


@dataclasses.dataclass
class Cache:
    last_weather_code: Optional[int] = None


cache = Cache()


def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(message)s",
    )


def update_profile_photo_from_weather():
    """
    Update the profile photo on slack based on the current weather condition.
    """
    try:
        sunrise_sunset = SunriseSunset.create(
            latitude=settings.latitude, longitude=settings.longitude
        )
        weather_code = weatherstack.get_current_weather_code(
            settings=settings.weatherstack,
            latitude=settings.latitude,
            longitude=settings.longitude,
            is_day=sunrise_sunset.is_day_now,
        )
        if cache.last_weather_code != weather_code:
            cache.last_weather_code = weather_code

            background_image_file = image.get_image_file(prefix=str(weather_code))
            foreground_image_file = Path(settings.profile_photos_dir) / (
                "photo.png" if sunrise_sunset.is_day_now else "night_photo.png"
            )
            profile_photo = image.create_profile_photo(
                background=background_image_file,
                foreground=foreground_image_file,
            )
            slack.set_profile_photo(settings.slack, profile_photo)
            logging.info(
                f"updated profile photo based on weather_code {weather_code}"
                + f" and background image {background_image_file}"
            )
        else:
            logging.info(f"No weather change since last time ({weather_code})")
    except Exception:
        logging.error("Error updating profile photo", exc_info=True)

    schedule.schedule(
        daytime_interval_s=settings.polling_interval_s,
        sunrise_sunset=sunrise_sunset,
        function=update_profile_photo_from_weather,
    )


if __name__ == "__main__":
    setup_logging()
    update_profile_photo_from_weather()
    Event().wait()
