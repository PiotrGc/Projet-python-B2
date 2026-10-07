import tkinter as tk
from PIL import Image, ImageTk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from datetime import date, datetime, timedelta

from constants import *
from weather import *
from weather_queries import *
from plot import *

# ----------------------------------------------------------------------
# Variables globales
# ----------------------------------------------------------------------
# Ville actuelle
city = "Paris"
# city = "Bordeaux"

# Premier jour affiché dans l'écran des prévisions
start_day = date.today()

# ImageTk : ces variables globales permettent d'éviter que le garbage collector ne les efface
image_background = None
weather_icon = None
forecast_icons = []

# Widgets Tkinter (boutons, graphique...) affichés sur l'écran actuel
widgets = []

# ----------------------------------------------------------------------
# Canvas
# ----------------------------------------------------------------------

def load_background(canvas):
    """Charge le ciel bleu (jour) ou le ciel étoilé (nuit), le redimensionne et le place sur le canvas."""
    global image_background

    if time_of_day() == "day":
        image = Image.open("assets/blue_sky.jpg").convert("RGBA")
    else:
        image = Image.open("assets/night_sky.jpg").convert("RGBA")
    image = image.resize((WIDTH, HEIGHT))
    image_background = ImageTk.PhotoImage(image)
    canvas.create_image(0, 0, image = image_background, anchor = "nw")


def load_icon(name, size):
    """Charge l'icône assets/icons/<name>.png à la taille demandée."""
    image = Image.open("assets/icons/" + name + ".png").convert("RGBA")
    image = image.resize((size, size))
    return ImageTk.PhotoImage(image)


def add_widget(canvas, x, y, widget):
    """Place un widget Tkinter sur le canvas et le mémorise pour pouvoir le détruire plus tard."""
    widgets.append(widget)
    canvas.create_window(x, y, window = widget, tags = "ecran")


def erase_screen(canvas):
    """Supprime tout ce qui a le tag 'ecran'."""
    canvas.delete("ecran")
    for widget in widgets:
        widget.destroy()
    widgets.clear()


def show_error(canvas, message):
    """Affiche un message d'erreur (ex : pas de connexion internet)."""
    canvas.create_text(WIDTH / 2, HEIGHT / 2, text = message, width = WIDTH - 40, justify = "center",
                       font = ("Helvetica", 14), fill = "white", tags = "ecran")


# ----------------------------------------------------------------------
# Ecrans
# ----------------------------------------------------------------------

def change_city(window, canvas, new_city):
    """Appelée par le menu déroulant : change de ville et redessine l'accueil."""
    global city
    city = new_city
    draw_welcome_screen(window, canvas)


def draw_welcome_screen(window, canvas):
    """Écran 1 : Icône de la météo, température actuelle, températures min et max du jour."""
    global weather_icon

    erase_screen(canvas)

    # Menu déroulant pour changer de ville
    city_variable = tk.StringVar(window, value = city)
    city_menu = tk.OptionMenu(window, city_variable, *CITIES.keys(),
                              command = lambda new_city: change_city(window, canvas, new_city))
    city_menu.config(font = ("Helvetica", 16, "bold"), width = 10)
    add_widget(canvas, WIDTH / 2, 45, city_menu)

    try:
        temperature, code, t_min, t_max = get_current_weather(city)
    except Exception as error:
        print(error)
        show_error(canvas, "Impossible de récupérer la météo.\nVérifiez votre connexion internet.")
        return

    # Icône de la météo (version nuit si besoin)
    icon = icon_of_code(code)
    if time_of_day() == "night":
        icon = night_icon(icon)
    if icon != "unknown":
        weather_icon = load_icon(icon, 160)
        canvas.create_image(WIDTH / 2, 170, image = weather_icon, tags = "ecran")

    canvas.create_text(WIDTH / 2, 300, text = f"{temperature:.1f} °C",
                       font = ("Helvetica", 44, "bold"), fill = "white", tags = "ecran")
    canvas.create_text(WIDTH / 2, 360, text = f"Min : {t_min:.1f} °C     Max : {t_max:.1f} °C",
                       font = ("Helvetica", 14), fill = "white", tags = "ecran")

    button = tk.Button(window, text = "Prévisions sur 7 jours", font = ("Helvetica", 12),
                       command = lambda : draw_forecast(window, canvas))
    add_widget(canvas, WIDTH / 2, 440, button)


def move_forecast(window, canvas, days):
    """Avance (days > 0) ou recule (days < 0) la période des prévisions."""
    global start_day
    start_day = start_day + timedelta(days = days)
    draw_forecast(window, canvas)


def draw_forecast(window, canvas):
    """Écran 2 : graphique des températures sur 7 jours"""
    global forecast_icons

    erase_screen(canvas)

    # Boutons : reculer de 7 jours, retour à l'accueil, avancer de 7 jours
    # (l'API n'accepte que les dates entre aujourd'hui - 92 jours et aujourd'hui + 15 jours)
    today = date.today()
    can_go_back = start_day - timedelta(days = 7) >= today - timedelta(days = MAX_PAST_DAYS)
    can_go_forward = start_day + timedelta(days = 13) <= today + timedelta(days = MAX_FUTURE_DAYS)

    button_left = tk.Button(window, text = "◀", width = 3,
                            command = lambda : move_forecast(window, canvas, -7))
    button_home = tk.Button(window, text = "Retour à l'accueil", font = ("Helvetica", 11),
                            command = lambda : draw_welcome_screen(window, canvas))
    button_right = tk.Button(window, text = "▶", width = 3,
                             command = lambda : move_forecast(window, canvas, 7))
    if not can_go_back:
        button_left.config(state = "disabled")
    if not can_go_forward:
        button_right.config(state = "disabled")
    add_widget(canvas, 40, 475, button_left)
    add_widget(canvas, WIDTH / 2, 475, button_home)
    add_widget(canvas, WIDTH - 40, 475, button_right)

    try:
        dates, t_mins, t_maxs, codes = get_forecast(city, start_day)
    except Exception as error:
        print(error)
        show_error(canvas, "Impossible de récupérer les prévisions.\nVérifiez votre connexion internet.")
        return

    # Titre, ville et période
    canvas.create_text(WIDTH / 2, 22, text = "Prévisions sur 7 jours",
                       font = ("Helvetica", 18, "bold"), fill = "white", tags = "ecran")
    canvas.create_text(WIDTH / 2, 48, text = city,
                       font = ("Helvetica", 14), fill = "white", tags = "ecran")
    first = datetime.strptime(dates[0], "%Y-%m-%d").strftime("%d/%m/%Y")
    last = datetime.strptime(dates[-1], "%Y-%m-%d").strftime("%d/%m/%Y")
    canvas.create_text(WIDTH / 2, 70, text = f"du {first} au {last}",
                       font = ("Helvetica", 11), fill = "white", tags = "ecran")

    # Icônes de la météo de chaque jour
    forecast_icons = []
    for i in range(len(codes)):
        icon = icon_of_code(codes[i])
        if icon == "unknown":
            continue
        image = load_icon(icon, 36)
        forecast_icons.append(image)
        x = 88 + i * 45 # aligné sur les dates du graphique
        canvas.create_image(x, 105, image = image, tags = "ecran")

    # Graphique Matplotlib
    figure = create_plot(dates, t_mins, t_maxs)
    zone_graphique = FigureCanvasTkAgg(figure, master = window)
    zone_graphique.draw()
    add_widget(canvas, WIDTH / 2, 290, zone_graphique.get_tk_widget())
