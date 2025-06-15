import tkinter as tk
import os
from PIL import Image, ImageTk

GRID_ROWS = 8
GRID_COLS = 8
BACKGROUND_IMAGE = "wilderness.png"

ICON_CATEGORIES = {
    "Bearbeitung": ["delete.png"],
    "Natur": [],
    "Tiere": [],
    "Charaktere": [],
    "Objekte": [],
}

for filename in os.listdir():
    if filename.endswith(".png"):
        if filename.startswith("Character_"):
            ICON_CATEGORIES["Charaktere"].append(filename)
        elif filename.startswith("Nature_"):
            ICON_CATEGORIES["Natur"].append(filename)
        elif filename.startswith("Objects_"):
            ICON_CATEGORIES["Objekte"].append(filename)
        elif filename.startswith("Animal_"):
            ICON_CATEGORIES["Tiere"].append(filename)

overlays = []
selected_icon_path = None
delete_mode = False
icon_images = {}

root = tk.Tk()
root.title("Digital Dungeons-And-Dragons")

bg_img = Image.open(BACKGROUND_IMAGE)
img_width, img_height = bg_img.size

screen_w, screen_h = root.winfo_screenwidth(), root.winfo_screenheight()
max_w, max_h = int(screen_w * 0.9), int(screen_h * 0.9)
scale = min(max_w / img_width, max_h / img_height, 1.0)

canvas_w = int(img_width * scale)
canvas_h = int(img_height * scale)

resized_bg = bg_img.resize((canvas_w, canvas_h), Image.LANCZOS)
tk_bg_img = ImageTk.PhotoImage(resized_bg)

main_frame = tk.Frame(root)
main_frame.pack(fill="both", expand=True)

left_panel = tk.Frame(main_frame)
left_panel.pack(side="left", fill="y", padx=10, pady=10)

canvas_frame = tk.Frame(main_frame)
canvas_frame.pack(side="right", expand=True)

canvas = tk.Canvas(canvas_frame, width=canvas_w, height=canvas_h)
canvas.pack()

canvas.create_image(0, 0, anchor="nw", image=tk_bg_img)

cell_w = canvas_w / GRID_COLS
cell_h = canvas_h / GRID_ROWS

for i in range(1, GRID_ROWS):
    y = i * cell_h
    canvas.create_line(0, y, canvas_w, y, fill="black", width=1.5)
for j in range(1, GRID_COLS):
    x = j * cell_w
    canvas.create_line(x, 0, x, canvas_h, fill="black", width=1.5)

def select_icon(path):
    global selected_icon_path, delete_mode
    selected_icon_path = path
    if path != "delete.png":
        set_delete_mode(False)

def set_delete_mode(active):
    global delete_mode, selected_icon_path
    delete_mode = active
    if active:
        selected_icon_path = None
        delete_btn.config(relief="sunken")
    else:
        delete_btn.config(relief="raised")

def on_canvas_click(event):
    col = int(event.x // cell_w)
    row = int(event.y // cell_h)

    if delete_mode:
        global overlays
        overlays = [o for o in overlays if not (o["row"] == row and o["col"] == col)]
        redraw_canvas()
    elif selected_icon_path:
        overlays.append({"path": selected_icon_path, "row": row, "col": col})
        draw_overlay(selected_icon_path, row, col)

def draw_overlay(path, row, col):
    if path not in icon_images:
        img = Image.open(path)
        img.thumbnail((cell_w * 0.8, cell_h * 0.8), Image.LANCZOS)
        icon_images[path] = ImageTk.PhotoImage(img)

    icon = icon_images[path]
    x = col * cell_w + cell_w / 2
    y = row * cell_h + cell_h / 2

    canvas.create_image(x, y, image=icon, anchor="center")

def redraw_canvas():
    canvas.delete("all")
    canvas.create_image(0, 0, anchor="nw", image=tk_bg_img)
    for i in range(1, GRID_ROWS):
        y = i * cell_h
        canvas.create_line(0, y, canvas_w, y, fill="black", width=1.5)
    for j in range(1, GRID_COLS):
        x = j * cell_w
        canvas.create_line(x, 0, x, canvas_h, fill="black", width=1.5)

    for o in overlays:
        draw_overlay(o["path"], o["row"], o["col"])

MAX_ICONS_PER_ROW = 12

for category, icons in ICON_CATEGORIES.items():
    label = tk.Label(left_panel, text=category, font=("Arial", 12, "bold"))
    label.pack(anchor="w", pady=(10, 0))

    btn_frame = tk.Frame(left_panel)
    btn_frame.pack(anchor="w", pady=5)

    for i, path in enumerate(icons):
        try:
            img = Image.open(path)
            img.thumbnail((60, 60))
            tk_icon = ImageTk.PhotoImage(img)
        except Exception as e:
            print(f"Fehler beim Laden von {path}: {e}")
            continue

        btn = tk.Button(btn_frame, image=tk_icon,
                        command=lambda p=path: select_icon(p))
        btn.image = tk_icon
        row = i // MAX_ICONS_PER_ROW
        col = i % MAX_ICONS_PER_ROW
        btn.grid(row=row, column=col, padx=3, pady=3)

        if path == "delete.png":
            delete_btn = btn

delete_btn.config(command=lambda: set_delete_mode(not delete_mode))

canvas.bind("<Button-1>", on_canvas_click)

root.mainloop()
