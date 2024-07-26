# open_meteo.py
import requests
import json
class OpenMeteo:
    BASE_URL = "https://api.open-meteo.com/v1/forecast"
    # https://api.open-meteo.com/v1/forecast?latitude=52.52&longitude=13.41&current=temperature_2m,wind_speed_10m&hourly=temperature_2m,relative_humidity_2m,wind_speed_10m
    @staticmethod
    def get_weather(latitude, longitude):
        params = {
            "latitude": 52.52,
            "longitude": 13.41,
            "current_weather": True,
            "current":"temperature_2m,wind_speed_10m",
            "hourly": "temperature_2m,relative_humidity_2m,wind_speed_10m"
        }
        response = requests.get(OpenMeteo.BASE_URL, params=params)
        response.raise_for_status()  # Raise an error for bad responses
        return response.json()
