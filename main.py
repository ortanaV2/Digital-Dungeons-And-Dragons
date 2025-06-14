import matplotlib.pyplot as plt
from PIL import Image
import numpy as np

def show_image_with_grid(image_path, rows, cols, overlays=[]):
    # Hintergrundbild laden
    bg_img = Image.open(image_path)
    width, height = bg_img.size
    bg_array = np.array(bg_img)

    # Plot vorbereiten
    fig, ax = plt.subplots()
    ax.imshow(bg_array)

    # Grid zeichnen
    for row in range(1, rows):
        y = row * height / rows
        ax.axhline(y=y, color='black', linewidth=1.5)

    for col in range(1, cols):
        x = col * width / cols
        ax.axvline(x=x, color='black', linewidth=1.5)

    # Overlays platzieren
    for overlay in overlays:
        place_image_in_cell(ax, overlay['path'], overlay['row'], overlay['col'], rows, cols, width, height)

    # Achsen auf Bildgröße fixieren (wichtiger Fix!)
    ax.set_xlim(0, width)
    ax.set_ylim(height, 0)

    ax.set_xticks([])
    ax.set_yticks([])
    plt.title(f"Grid: {rows} x {cols}")
    plt.show()


def place_image_in_cell(ax, image_path, cell_row, cell_col, total_rows, total_cols, total_width, total_height):
    cell_width = total_width / total_cols
    cell_height = total_height / total_rows

    center_x = (cell_col + 0.5) * cell_width
    center_y = (cell_row + 0.5) * cell_height

    img = Image.open(image_path)
    img.thumbnail((cell_width * 0.8, cell_height * 0.8), Image.LANCZOS)
    img_array = np.array(img)

    x0 = center_x - img.width / 2
    y0 = center_y - img.height / 2

    ax.imshow(img_array, extent=(x0, x0 + img.width, y0 + img.height, y0), zorder=10)


# Beispiel: mehrere Bilder in Zellen platzieren
overlays = [
    {"path": "icon.png", "row": 2, "col": 3},
    {"path": "icon.png", "row": 5, "col": 1},
    {"path": "icon.png", "row": 0, "col": 0},
]

show_image_with_grid("wilderness.png", rows=8, cols=8, overlays=overlays)
