import requests
from pydantic import BaseModel


class WeatherstackSettings(BaseModel):
    api_access_key: str


def get_current_weather_code(
    settings: WeatherstackSettings,
    latitude: float,
    longitude: float,
    is_day: bool,
) -> int:
    """
    :return: The weather_code for the current condition at the location defined
    in the environment variable.
    """
    if not is_day:
        return 999
    response = requests.get(
        url="http://api.weatherstack.com/current",
        params={
            "access_key": settings.api_access_key,
            "query": f"{latitude},{longitude}",
        },
    )
    response_data: dict = response.json()
    if response_data.get("success") is False:
        raise Exception(response_data["error"])
    return response_data["current"]["weather_code"]
