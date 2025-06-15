import tkinter as tk
from tkinter import filedialog
import os
from PIL import Image, ImageTk

GRID_ROWS = 8
GRID_COLS = 8
BACKGROUND_IMAGE = "Wilderness - 8x8.png"

ICON_CATEGORIES = {
    "Bearbeitung": ["delete.png"],
    "Natur": [],
    "Tiere": [],
    "Charaktere": [],
    "Objekte": [],
}

# Icons automatisch einsortieren
for filename in os.listdir():
    if filename.endswith(".png"):
        if filename.startswith("Character_"):
            ICON_CATEGORIES["Charaktere"].append(filename)
        elif filename.startswith("Nature_"):
            ICON_CATEGORIES["Natur"].append(filename)
        elif filename.startswith("Object_"):
            ICON_CATEGORIES["Objekte"].append(filename)
        elif filename.startswith("Animal_"):
            ICON_CATEGORIES["Tiere"].append(filename)

# Tooltip-Klasse
class ToolTip:
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tooltip = None
        self.widget.bind("<Enter>", self.show)
        self.widget.bind("<Leave>", self.hide)

    def show(self, event=None):
        if self.tooltip or not self.text:
            return
        x = self.widget.winfo_rootx() + 40
        y = self.widget.winfo_rooty() + 10
        self.tooltip = tk.Toplevel(self.widget)
        self.tooltip.overrideredirect(True)
        self.tooltip.geometry(f"+{x}+{y}")
        label = tk.Label(self.tooltip, text=self.text, bg="white", relief="solid",
                         borderwidth=1, font=("Arial", 10), padx=4, pady=2)
        label.pack()

    def hide(self, event=None):
        if self.tooltip:
            self.tooltip.destroy()
            self.tooltip = None

# Globale Variablen
overlays = []
selected_icon_path = None
delete_mode = False
icon_images = {}

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
        delete_overlay_at(row, col)
    elif selected_icon_path:
        overlays.append({"path": selected_icon_path, "row": row, "col": col})
        draw_overlay(selected_icon_path, row, col)

def on_canvas_right_click(event):
    col = int(event.x // cell_w)
    row = int(event.y // cell_h)
    delete_overlay_at(row, col)

def delete_overlay_at(row, col):
    global overlays
    overlays = [o for o in overlays if not (o["row"] == row and o["col"] == col)]
    redraw_canvas()

def draw_overlay(path, row, col):
    if path not in icon_images:
        no_padding_objects = ["Object_Tree", "Object_Rock_Stone", "Object_Rock_Dirt"]
        padding = 1.0 if any(name in path for name in no_padding_objects) else 0.8
        img = Image.open(path)
        img.thumbnail((cell_w * padding, cell_h * padding), Image.LANCZOS)
        icon_images[path] = ImageTk.PhotoImage(img)

    icon = icon_images[path]
    x = col * cell_w + cell_w / 2
    y = row * cell_h + cell_h / 2
    canvas.create_image(x, y, image=icon, anchor="center", tags=("icon_" + os.path.basename(path),))

def redraw_canvas():
    global cell_w, cell_h
    canvas.delete("all")
    canvas.create_image(0, 0, anchor="nw", image=tk_bg_img)
    cell_w = canvas_w / GRID_COLS
    cell_h = canvas_h / GRID_ROWS
    for i in range(1, GRID_ROWS):
        y = i * cell_h
        canvas.create_line(0, y, canvas_w, y, fill="black", width=1.5)
    for j in range(1, GRID_COLS):
        x = j * cell_w
        canvas.create_line(x, 0, x, canvas_h, fill="black", width=1.5)
    for o in overlays:
        draw_overlay(o["path"], o["row"], o["col"])

def change_map():
    global tk_bg_img, bg_img, canvas_w, canvas_h, canvas, cell_w, cell_h, GRID_ROWS, GRID_COLS
    file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
    if not file_path:
        return
    try:
        bg_img = Image.open(file_path)
    except Exception as e:
        print("Fehler beim Laden des Bilds:", e)
        return

    try:
        GRID_ROWS = int(entry_rows.get())
        GRID_COLS = int(entry_cols.get())
    except ValueError:
        print("Ungültige Eingabe für Grid-Größe.")
        return

    img_width, img_height = bg_img.size
    screen_w, screen_h = root.winfo_screenwidth(), root.winfo_screenheight()
    max_w, max_h = int(screen_w * 0.9), int(screen_h * 0.9)
    scale = min(max_w / img_width, max_h / img_height, 1.0)

    canvas_w = int(img_width * scale)
    canvas_h = int(img_height * scale)
    resized_bg = bg_img.resize((canvas_w, canvas_h), Image.LANCZOS)
    tk_bg_img = ImageTk.PhotoImage(resized_bg)

    canvas.config(width=canvas_w, height=canvas_h)
    redraw_canvas()
    icon_images.clear()

# Hauptfenster
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

top_controls = tk.Frame(main_frame)
top_controls.pack(side="top", anchor="ne", padx=10, pady=5)

tk.Label(top_controls, text="Zeilen:").pack(side="left")
entry_rows = tk.Entry(top_controls, width=4)
entry_rows.insert(0, str(GRID_ROWS))
entry_rows.pack(side="left", padx=5)

tk.Label(top_controls, text="Spalten:").pack(side="left")
entry_cols = tk.Entry(top_controls, width=4)
entry_cols.insert(0, str(GRID_COLS))
entry_cols.pack(side="left", padx=5)

btn_map = tk.Button(top_controls, text="Change Map", command=change_map)
btn_map.pack(side="left", padx=10)

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

        btn = tk.Button(btn_frame, image=tk_icon, command=lambda p=path: select_icon(p))
        btn.image = tk_icon
        row = i // MAX_ICONS_PER_ROW
        col = i % MAX_ICONS_PER_ROW
        btn.grid(row=row, column=col, padx=3, pady=3)

        ToolTip(btn, os.path.basename(path))  # Tooltip für Button

        if path == "delete.png":
            delete_btn = btn

delete_btn.config(command=lambda: set_delete_mode(not delete_mode))

canvas.bind("<Button-1>", on_canvas_click)
canvas.bind("<Button-3>", on_canvas_right_click)

tooltip = tk.Label(canvas, text="", bg="white", relief="solid", borderwidth=1, font=("Arial", 10), padx=4, pady=2)
tooltip.place_forget()

def on_mouse_move(event):
    items = canvas.find_overlapping(event.x, event.y, event.x, event.y)
    for item in items:
        tag = canvas.gettags(item)
        if tag and tag[0].startswith("icon_"):
            icon_name = tag[0][5:]
            tooltip.config(text=icon_name)
            tooltip.place(x=event.x + 15, y=event.y + 10)
            return
    tooltip.place_forget()

canvas.bind("<Motion>", on_mouse_move)

root.mainloop()
