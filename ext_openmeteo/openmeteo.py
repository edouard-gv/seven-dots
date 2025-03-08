import time

import requests_cache
from retry_requests import retry


class OpenMeteo:
    def __init__(self):
        cache_session = requests_cache.CachedSession('.cache', expire_after=3600)
        retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
        self.session = retry_session
        self.__wma_ww_code_map = {
            '0': 'bleu +',
            '1': 'bleu',
            '2': 'bleu -',
            '3': 'couvert',
            '45': 'brouil',
            '48': 'brouil',
            '51': 'bruine',
            '53': 'bruine+',
            '55': 'bruin++',
            '56': 'bruine',
            '57': 'bruin++',
            '61': 'pluie',
            '63': 'pluie+',
            '65': 'pluie++',
            '66': 'pluie v',
            '67': 'pluie+v',
            '71': 'neige',
            '73': 'neige+',
            '75': 'neige++',
            '77': 'grele',
            '80': 'averses',
            '81': 'averse+',
            '82': 'avers++',
            '85': 'neige+',
            '86': 'neige++',
            '95': 'orage',
            '96': 'ora+gre',
            '99': 'or++gre'
        }

    def weather_api(self):
        url = "https://api.open-meteo.com/v1/forecast"
        params = {
            "latitude": 48.97,
            "longitude": 3.32,
            "current": "apparent_temperature",
            "daily": ["weather_code", "apparent_temperature_max", "apparent_temperature_min", "sunrise", "sunset"],
            "timezone": "Europe/Berlin",
            "past_days": 1,
            "forecast_days": 1
        }
        response = self.session.get(url, params=params).json()
        return response

    def convert_weather_code(self, code):
        if str(code) not in self.__wma_ww_code_map:
            return str(code)
        return self.__wma_ww_code_map[str(code)]

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
                self.convert_weather_code(data["daily"]["weather_code"][1]),
                "%.1f C" % data["current"]["apparent_temperature"],
                str(round(data["daily"]["apparent_temperature_min"][1])) + "_" + str(round(
                    data["daily"]["apparent_temperature_max"][1])),
                str(round(data["daily"]["apparent_temperature_max"][1] - data["daily"]["apparent_temperature_max"][0])),
            ]]
