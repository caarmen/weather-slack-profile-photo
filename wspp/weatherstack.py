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
        url="http://api.weatherstack.com/current",
        params={
            "access_key": api_access_key,
            "query": f"{latitude},{longitude}",
        },
    )
    response_data: dict = response.json()
    if response_data.get("success") is False:
        raise Exception(response_data["error"])
    return response_data["current"]["weather_code"]
