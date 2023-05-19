import logging
from threading import Timer
from typing import Callable

from wspp.sunrisesunset import SunriseSunset


def schedule(
    daytime_interval_s: int,
    sunrise_sunset: SunriseSunset,
    function: Callable[[], None],
):
    """
    Schedule the given function to be executed in the given interval if it's
    day right now, otherwise when the next sunrise occurs.
    """
    delay_s = (
        daytime_interval_s
        if sunrise_sunset.is_day_now
        else sunrise_sunset.seconds_until_next_sunrise
    )
    logging.info(f"Scheduling next poll in {delay_s} seconds")
    timer = Timer(delay_s, function)
    timer.daemon = True
    timer.start()
