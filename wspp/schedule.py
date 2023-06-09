import logging
from threading import Timer
from typing import Callable

from wspp.sunrisesunset import SunriseSunset

# Small buffer to be SURE our function is called after sunrise (or sunset)
BUFFER_SUNRISE_SUNSET_DELAY_S = 120


def schedule(
    daytime_interval_s: int,
    sunrise_sunset: SunriseSunset,
    function: Callable[[], None],
):
    """
    Schedule the given function to be executed in the given interval if it's
    day right now, otherwise when the next sunrise occurs.
    """
    if sunrise_sunset.is_day_now:
        if daytime_interval_s > sunrise_sunset.seconds_until_next_sunset:
            delay_s = (
                sunrise_sunset.seconds_until_next_sunset + BUFFER_SUNRISE_SUNSET_DELAY_S
            )
            logging.info(
                f"Scheduling next poll in {delay_s} seconds, when the sun will set"
            )
        else:
            delay_s = daytime_interval_s
            logging.info(f"Scheduling next poll in {delay_s} seconds")
    else:
        delay_s = (
            sunrise_sunset.seconds_until_next_sunrise + BUFFER_SUNRISE_SUNSET_DELAY_S
        )
        logging.info(
            f"Scheduling next poll in {delay_s} seconds, when the sun will rise"
        )
    timer = Timer(delay_s, function)
    timer.daemon = True
    timer.start()
