"""
Script which periodically:
* fetches the weather condition of a specified location, 
* selects a background image based on the weather condition,
* creates a new profile photo using this background image and a provided profile photo,
* and updates the user's profile photo in Slack with this new profile photo.
"""

import dataclasses
import io
import logging
from pathlib import Path
from threading import Event, Timer
from typing import Optional
from pydantic import BaseSettings, DirectoryPath, FilePath, PositiveInt
import requests
from PIL import Image


class Settings(BaseSettings):
    weatherstack_api_access_key: str
    slack_token: str
    slack_cookie_d: str
    slack_workspace: str
    latitude: float
    longitude: float
    profile_photo_path: FilePath = Path(__file__).parent / "photo.png"
    resources_dir: DirectoryPath = Path(__file__).parent / "resources"
    polling_interval_s: PositiveInt = 3600

    class Config:
        env_file = ".env"


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


def get_current_weather_code() -> int:
    """
    :return: The weather_code for the current condition at the location defined
    in the environment variable.
    """
    response = requests.get(
        url="http://api.weatherstack.com/current",
        params={
            "access_key": settings.weatherstack_api_access_key,
            "query": f"{settings.latitude},{settings.longitude}",
        },
    )
    response_data: dict = response.json()
    if response_data.get("success") is False:
        raise Exception(response_data["error"])
    return response_data["current"]["weather_code"]


def get_background_image_file(weather_code: int) -> Path:
    """
    :return: the background image file corresponding to the given weather code.
    """
    return next(settings.resources_dir.glob(f"{weather_code}*"))


def create_profile_photo(background: Path) -> io.BytesIO:
    """
    :return: the binary data of an image containing the given background image, with
    the photo provided in PROFILE_PHOTO_PATH on top.
    """
    background_image = Image.open(background)
    foreground_image = Image.open(Path(settings.profile_photo_path)).convert("RGBA")
    new_image = Image.new(
        mode="RGB",
        size=background_image.size,
    )
    new_image.paste(background_image)
    new_image.paste(foreground_image, (0, 0), foreground_image)
    bio = io.BytesIO()
    new_image.save(bio, format="JPEG")
    bio.seek(0)
    return bio


def set_profile_photo(image_data: io.BytesIO):
    """
    Update the profile photo on slack with the given image.
    """
    response = requests.post(
        url=f"https://{settings.slack_workspace}/api/users.setPhoto",
        headers={
            "cookie": f"d={settings.slack_cookie_d}",
        },
        data={
            "token": settings.slack_token,
        },
        files=[("image", ("photo.jpg", image_data, "image/jpeg"))],
    )
    response_data: dict = response.json()
    if response_data.get("ok") is False:
        raise Exception(f"Error updating photo: {response_data.get('error')}")


def update_profile_photo_from_weather():
    """
    Update the profile photo on slack based on the current weather condition.
    """
    try:
        weather_code = get_current_weather_code()
        if cache.last_weather_code != weather_code:
            cache.last_weather_code = weather_code
            background_image_file = get_background_image_file(weather_code)
            profile_photo = create_profile_photo(background=background_image_file)
            set_profile_photo(profile_photo)
            logging.info(
                f"updated profile photo based on weather_code {weather_code}"
                + f" and background image {background_image_file}"
            )
        else:
            logging.info(f"No weather change since last time ({weather_code})")
    except Exception:
        logging.error("Error updating profile photo", exc_info=True)
    schedule_update_profile_photo()


def schedule_update_profile_photo():
    timer = Timer(settings.polling_interval_s, update_profile_photo_from_weather)
    timer.daemon = True
    timer.start()


if __name__ == "__main__":
    setup_logging()
    update_profile_photo_from_weather()
    Event().wait()
