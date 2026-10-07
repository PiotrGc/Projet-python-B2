from matplotlib.figure import Figure

# ----------------------------------------------------------------------
# Plot Matplotlib
# ----------------------------------------------------------------------

def create_plot(dates, temperatures_min, temperatures_max):
    """Crée et retourne une Figure Matplotlib avec les courbes de températures min et max sur les dates fournies."""
    figure = Figure(figsize = (3.8, 3.2))
    axes = figure.add_subplot(111)

    ######################################

    x = range(len(dates))
    axes.plot(x, temperatures_max, color = "tab:red", marker = "o", label = "Max")
    axes.plot(x, temperatures_min, color = "tab:blue", marker = "o", label = "Min")
    axes.fill_between(x, temperatures_min, temperatures_max, color = "orange", alpha = 0.15)
    axes.set_ylabel("Température (°C)")
    axes.grid(True, alpha = 0.3)
    axes.legend(fontsize = 8)

    ######################################

    # Améliore la lisibilité
    axes.set_xticks(range(len(dates)))
    axes.set_xticklabels([d[5:] for d in dates], rotation = 45)
    figure.tight_layout()

    return figure
