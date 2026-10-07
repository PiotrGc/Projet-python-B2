# ----------------------------------------------------------------------
# Constantes
# ----------------------------------------------------------------------

CITIES = {
    "Paris":        (48.8566,  2.3522),
    "Marseille":    (43.2965,  5.3698),
    "Lyon":         (45.7640,  4.8357),
    "Toulouse":     (43.6047,  1.4442),
    "Bordeaux":     (44.8378, -0.5792),
    "Lille":        (50.6292,  3.0573),
    "Nantes":       (47.2184, -1.5536),
    "Strasbourg":   (48.5734,  7.7521),
    "Rennes":       (48.1173, -1.6778),
    "Grenoble":     (45.1885,  5.7245),
}

WIDTH = 400
HEIGHT = 500
URL_API = "https://api.open-meteo.com/v1/forecast"

# Limites de l'API Open-Meteo (endpoint "forecast") pour start_date / end_date
MAX_PAST_DAYS = 92
MAX_FUTURE_DAYS = 15
