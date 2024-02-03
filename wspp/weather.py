from wspp import weatherapi, weatherstack
from wspp.settings import ProviderName, Settings


def get_current_weather_code(
    settings: Settings,
    is_day: bool,
) -> int:
    """
    :return: The weather_code for the current condition at the location defined
    in the environment variable.
    """
    if not is_day:
        return 999

    if settings.weatherprovider.name == ProviderName.WEATHERSTACK:
        provider_function = weatherstack.get_current_weather_code
    else:
        provider_function = weatherapi.get_current_weather_code

    return provider_function(
        api_access_key=settings.weatherprovider.api_access_key,
        latitude=settings.wspp.latitude,
        longitude=settings.wspp.longitude,
    )
