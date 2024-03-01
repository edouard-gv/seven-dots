import time

import requests_cache
from retry_requests import retry


class OpenMeteo:
    def __init__(self):
        cache_session = requests_cache.CachedSession('.cache', expire_after=3600)
        retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
        self.session = retry_session

    def weather_api(self):
        url = "https://api.open-meteo.com/v1/forecast"
        params = {
            "latitude": 48.8,
            "longitude": 2.33,
            "current": "apparent_temperature",
            "daily": ["weather_code", "apparent_temperature_max", "apparent_temperature_min", "sunrise", "sunset"],
            "timezone": "Europe/Berlin",
            "past_days": 1,
            "forecast_days": 1
        }
        response = self.session.get(url, params=params).json()
        return response

    def current_time(self):
        # return time in iso8601 format
        return time.strftime("%Y-%m-%dT%H:%M", time.localtime())

    def format_time(self, iso_date):
        return iso_date.split("T")[1].lstrip("0")

    def format_short_date(self, iso_date):
        md_date = iso_date[5:10].split("-")
        return md_date[1] + "-" + md_date[0]

    def weather_views(self):
        data = self.weather_api()
        return [
            [
                self.format_short_date(self.current_time()),
                self.format_time(self.current_time()),
                self.format_time(data["daily"]["sunrise"][1]),
                self.format_time(data["daily"]["sunset"][1]),
            ], [
                str(data["daily"]["weather_code"][1]),
                "%.1f C" % data["current"]["apparent_temperature"],
                str(round(data["daily"]["apparent_temperature_min"][1])) + " - " + str(round(
                    data["daily"]["apparent_temperature_max"][1])),
                str(round(data["daily"]["apparent_temperature_max"][1] - data["daily"]["apparent_temperature_max"][0])),
            ]]
