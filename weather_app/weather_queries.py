import requests
from datetime import timedelta

from constants import *

# ----------------------------------------------------------------------
# Requêtes d'API Open-Meteo
# ----------------------------------------------------------------------

def get_current_weather(city):
    """Retourne (température actuelle, code météo, t_min du jour, t_max du jour)."""

    parameters = {
        # ...
        "timezone": "auto",
        "forecast_days": 1,
    }
    response = requests.get(URL_API, params = parameters, timeout = 10)
    data = response.json()

    temperature_now, code, t_min_today, t_max_today = 0, 0, 0, 0 # TODO
    # ...
    return temperature_now, code, t_min_today, t_max_today


def get_forecast(city, start_day):
    """Retourne (dates, temperatures_min, temperatures_max) pour 7 jours à partir de start_day."""
    end_day = start_day # + ...

    parameters = {
        # ...
        "start_date": start_day.isoformat(), # pour avoir le format "2025-01-31"
        "end_date": end_day.isoformat(),
        "timezone": "auto",
    }
    response = requests.get(URL_API, params = parameters, timeout = 10)
    data = response.json()

    dates, temperatures_min, temperatures_max = [], [], [] # TODO
    return dates, temperatures_min, temperatures_max