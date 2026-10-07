import requests
from datetime import timedelta

from constants import *

# ----------------------------------------------------------------------
# Requêtes d'API Open-Meteo
# ----------------------------------------------------------------------

def get_current_weather(city):
    """Retourne (température actuelle, code météo, t_min du jour, t_max du jour)."""
    latitude, longitude = CITIES[city]

    parameters = {
        "latitude": latitude,
        "longitude": longitude,
        "current": "temperature_2m,weather_code",
        "daily": "temperature_2m_max,temperature_2m_min",
        "timezone": "auto",
        "forecast_days": 1,
    }
    response = requests.get(URL_API, params = parameters, timeout = 10)
    response.raise_for_status()
    data = response.json()
    print(data)

    temperature_now = data["current"]["temperature_2m"]
    code = data["current"]["weather_code"]
    t_min_today = data["daily"]["temperature_2m_min"][0]
    t_max_today = data["daily"]["temperature_2m_max"][0]
    return temperature_now, code, t_min_today, t_max_today


def get_forecast(city, start_day):
    """Retourne (dates, temperatures_min, temperatures_max, codes) pour 7 jours à partir de start_day."""
    latitude, longitude = CITIES[city]
    end_day = start_day + timedelta(days = 6)

    parameters = {
        "latitude": latitude,
        "longitude": longitude,
        "daily": "temperature_2m_max,temperature_2m_min,weather_code",
        "start_date": start_day.isoformat(), # pour avoir le format "2025-01-31"
        "end_date": end_day.isoformat(),
        "timezone": "auto",
    }
    response = requests.get(URL_API, params = parameters, timeout = 10)
    response.raise_for_status()
    data = response.json()

    dates = data["daily"]["time"]
    temperatures_min = data["daily"]["temperature_2m_min"]
    temperatures_max = data["daily"]["temperature_2m_max"]
    codes = data["daily"]["weather_code"]
    return dates, temperatures_min, temperatures_max, codes
