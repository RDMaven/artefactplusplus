import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np


def display_robot(x: float, y: float, theta: float, ax=None, fig=None):
    """
    Affiche en temps réel la position et l'orientation d'un robot sur un terrain 1000x1000.

    Args:
        x     : position X du robot  (entre -500 et 500)
        y     : position Y du robot  (entre -500 et 500)
        theta : orientation en radians (0 = vers la droite, sens anti-horaire)

    Returns:
        fig, ax : les objets matplotlib pour réutilisation
    """
    # Initialisation de la figure (uniquement au premier appel)
    if fig is None or ax is None:
        plt.ion()  # mode interactif → pas de blocage
        fig, ax = plt.subplots(figsize=(7, 7))
        fig.patch.set_facecolor("#0d1117")

    ax.clear()

    # ── Fond et grille ────────────────────────────────────────────────────────
    ax.set_facecolor("#0d1117")
    ax.set_xlim(-520, 520)
    ax.set_ylim(-520, 520)
    ax.set_aspect("equal")

    # Quadrillage discret
    grid_ticks = np.arange(-500, 501, 100)
    for v in grid_ticks:
        ax.axhline(v, color="#1e2d3d", linewidth=0.6, zorder=1)
        ax.axvline(v, color="#1e2d3d", linewidth=0.6, zorder=1)

    # Axes centraux
    ax.axhline(0, color="#2e4a6a", linewidth=1.2, zorder=2)
    ax.axvline(0, color="#2e4a6a", linewidth=1.2, zorder=2)

    # Bordure du terrain
    border = plt.Rectangle((-500, -500), 1000, 1000,
                            linewidth=2, edgecolor="#00aaff",
                            facecolor="none", zorder=3)
    ax.add_patch(border)

    # ── Robot ─────────────────────────────────────────────────────────────────
    robot_radius = 18  # rayon du cercle représentant le robot

    # Corps (cercle)
    robot_body = plt.Circle((x, y), robot_radius,
                             color="#00aaff", zorder=5, alpha=0.9)
    ax.add_patch(robot_body)

    # Halo lumineux
    glow = plt.Circle((x, y), robot_radius * 1.6,
                       color="#00aaff", zorder=4, alpha=0.12)
    ax.add_patch(glow)

    # Flèche d'orientation
    arrow_len = robot_radius * 1.8
    dx = arrow_len * np.cos(theta)
    dy = arrow_len * np.sin(theta)
    ax.annotate(
        "", xy=(x + dx, y + dy), xytext=(x, y),
        arrowprops=dict(
            arrowstyle="-|>",
            color="#ff6b35",
            lw=2.5,
            mutation_scale=18,
        ),
        zorder=6,
    )

    # ── Étiquettes ────────────────────────────────────────────────────────────
    theta_deg = np.degrees(theta) % 360
    info = f"x = {x:.1f}   y = {y:.1f}   θ = {theta_deg:.1f}°"
    ax.text(0, -545, info,
            ha="center", va="center", fontsize=11,
            color="#c9d1d9", fontfamily="monospace",
            bbox=dict(boxstyle="round,pad=0.4", facecolor="#161b22",
                      edgecolor="#00aaff", linewidth=1))

    # Légende des axes
    for label, lx, ly in [("X", 510, 8), ("-X", -520, 8),
                           ("Y", 8, 510), ("-Y", 8, -520)]:
        ax.text(lx, ly, label, color="#2e4a6a", fontsize=8,
                ha="center", fontfamily="monospace")

    ax.set_title("Robot Tracker", color="#c9d1d9",
                 fontsize=13, pad=10, fontfamily="monospace")
    ax.tick_params(colors="#2e4a6a", labelsize=7)
    for spine in ax.spines.values():
        spine.set_edgecolor("#1e2d3d")

    fig.tight_layout()
    fig.canvas.draw()
    fig.canvas.flush_events()

    return fig, ax


# ── Exemple d'utilisation ─────────────────────────────────────────────────────
if __name__ == "__main__":
    import time

    fig, ax = None, None

    # Simulation : le robot avance en spirale
    for t in np.linspace(0, 4 * np.pi, 200):
        robot_x = 200 * np.cos(t) * (t / (4 * np.pi))
        robot_y = 200 * np.sin(t) * (t / (4 * np.pi))
        robot_theta = t + np.pi / 2          # tangent à la trajectoire

        fig, ax = display_robot(robot_x, robot_y, robot_theta, ax, fig)
        time.sleep(0.04)

    plt.ioff()
    plt.show()