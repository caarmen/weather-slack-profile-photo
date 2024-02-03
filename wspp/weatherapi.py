import re

import requests


def get_current_weather_code(
    api_access_key: str,
    latitude: float,
    longitude: float,
) -> int:
    """
    :return: The weather_code for the current condition at the location defined
    in the environment variable.
    """
    response = requests.get(
        url="http://api.weatherapi.com/v1/current.json",
        params={
            "key": api_access_key,
            "q": f"{latitude},{longitude}",
            "aqi": "no",
        },
    )
    if not response.ok:
        raise Exception(response.text)
    response_data: dict = response.json()
    # ex: //cdn.weatherapi.com/weather/64x64/day/248.png
    icon = response_data["current"]["condition"]["icon"]
    pattern = re.compile(r"^.*/([0-9]*).png$")
    tokens = pattern.findall(icon)
    code = tokens[-1]

    return code
