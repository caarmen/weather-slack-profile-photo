import dataclasses
import datetime
import logging
from functools import cached_property
from typing import Self

from astral import LocationInfo, sun


@dataclasses.dataclass
class SunriseSunset:
    location: LocationInfo
    sunrise: datetime.datetime
    sunset: datetime.datetime

    @classmethod
    def create(cls, latitude: float, longitude: float) -> Self:
        location = LocationInfo(latitude=latitude, longitude=longitude)
        try:
            sunrise = sun.sunrise(observer=location.observer)
            sunset = sun.sunset(observer=location.observer)
        except ValueError as e:
            # https://github.com/sffjunkie/astral/issues/64
            logging.info(
                f"Couldn't calculate sunrise or sunset. Polar zone detected? {e}"
            )
            # If we can't figure out sunrise/sunset, just pretend it's day all day.
            sunrise = datetime.datetime.now(tz=datetime.timezone.utc).replace(
                hour=0, minute=0, second=0, microsecond=0
            )
            sunset = sunrise + datetime.timedelta(days=1)
        return cls(location=location, sunrise=sunrise, sunset=sunset)

    @cached_property
    def is_day_now(self):
        now = datetime.datetime.now(datetime.timezone.utc)
        return self.sunrise < now < self.sunset

    @cached_property
    def seconds_until_next_sunrise(self):
        now = datetime.datetime.now(tz=datetime.timezone.utc)
        # Ex: it's 2am now, and the sun will rise in 4 hours at 6am:
        if self.sunrise > now:
            return (self.sunrise - now).seconds
        # Ex: the sun rose at 6am, and it's now 10am, and the sun will
        # rise tomorrow at 6am
        tomorrow = now + datetime.timedelta(days=1)
        tomorrow_data = sun.sun(observer=self.location.observer, date=tomorrow.date())
        return (tomorrow_data["sunrise"] - now).seconds

    @cached_property
    def seconds_until_next_sunset(self):
        now = datetime.datetime.now(tz=datetime.timezone.utc)
        # Ex: it's noon now, and the sun will set in 6 hours at 6pm:
        if self.sunset > now:
            return (self.sunset - now).seconds
        # Ex: the sun set at 6pm, and it's now 10pm, and the sun will
        # set tomorrow at 6pm
        tomorrow = now + datetime.timedelta(days=1)
        tomorrow_data = sun.sun(observer=self.location.observer, date=tomorrow.date())
        return (tomorrow_data["sunset"] - now).seconds
