from datetime import datetime

# ----------------------------------------------------------------------
# Météo
# ----------------------------------------------------------------------

def icon_of_code(code):
    """Obtient le nom d'icône correspondant au code météo (WMO) d'Open-Meteo."""
    if code == 0:
        return "sunny"
    if code in (1, 2):
        return "partly_cloudy_day"
    if code == 3:
        return "cloudy"
    if code in (45, 48):
        return "fog"
    if code in (51, 53, 55, 56, 57, 61, 63, 65, 66, 67, 80, 81, 82):
        return "rain"
    if code in (71, 73, 75, 77, 85, 86):
        return "snow"
    if code in (95, 96, 99):
        return "storm"
    return "unknown"

def time_of_day():
    """Renvoie "day" ou "night" en fonction de l'heure de la journée"""
    # TODO
    pass
