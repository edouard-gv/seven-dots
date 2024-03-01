from ext_openmeteo.openmeteo import OpenMeteo

typical_output = {
    "latitude": 48.8,
    "longitude": 2.3399997,
    "generationtime_ms": 0.13303756713867188,
    "utc_offset_seconds": 3600,
    "timezone": "Europe/Berlin",
    "timezone_abbreviation": "CET",
    "elevation": 60,
    "current_units": {
        "time": "iso8601",
        "interval": "seconds",
        "apparent_temperature": "°C"
    },
    "current": {
        "time": "2024-03-01T14:30",
        "interval": 900,
        "apparent_temperature": 6.2
    },
    "daily_units": {
        "time": "iso8601",
        "weather_code": "wmo code",
        "apparent_temperature_max": "°C",
        "apparent_temperature_min": "°C",
        "sunrise": "iso8601",
        "sunset": "iso8601"
    },
    "daily": {
        "time": [
            "2024-02-29",
            "2024-03-01"
        ],
        "weather_code": [
            61,
            80
        ],
        "apparent_temperature_max": [
            8.1,
            6.7
        ],
        "apparent_temperature_min": [
            4.1,
            0.2
        ],
        "sunrise": [
            "2024-02-29T07:33",
            "2024-03-01T07:31"
        ],
        "sunset": [
            "2024-02-29T18:32",
            "2024-03-01T18:34"
        ]
    }
}


def mocked_meteo_service():
    meteo_service = OpenMeteo()
    meteo_service.weather_api = lambda: typical_output
    meteo_service.current_time = lambda: "2024-03-01T14:37"
    return meteo_service


def test_mock():
    meteo_service = mocked_meteo_service()
    assert meteo_service.weather_api() == typical_output


def test_meteo_service_4lines_views():
    meteo_service = mocked_meteo_service()
    views = meteo_service.weather_views()
    assert views[0] == ["01-03", "14:37", "7:31", "18:34"]
    assert views[1] == ["douches", "6.2 C", "0_7", "-1"]