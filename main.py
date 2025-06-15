import tkinter as tk
from tkinter import filedialog
import os
from PIL import Image, ImageTk

ICON_FOLDER = "icon_pack"
BACKGROUND_IMAGE = os.path.join(ICON_FOLDER, "Wilderness - 8x8.png")

GRID_ROWS = 8
GRID_COLS = 8

ICON_CATEGORIES = {
    "Bearbeitung": ["delete.png"],
    "Natur": [],
    "Tiere": [],
    "Charaktere": [],
    "Objekte": [],
}

for filename in os.listdir(ICON_FOLDER):
    if filename.endswith(".png"):
        full_path = os.path.join(ICON_FOLDER, filename)
        if filename.startswith("Character_"):
            ICON_CATEGORIES["Charaktere"].append(full_path)
        elif filename.startswith("Nature_"):
            ICON_CATEGORIES["Natur"].append(full_path)
        elif filename.startswith("Object_"):
            ICON_CATEGORIES["Objekte"].append(full_path)
        elif filename.startswith("Animal_"):
            ICON_CATEGORIES["Tiere"].append(full_path)
        elif filename == "delete.png":
            ICON_CATEGORIES["Bearbeitung"][0] = full_path

overlays = []
selected_icon_path = None
delete_mode = False
icon_images = {}

def select_icon(path):
    global selected_icon_path, delete_mode
    selected_icon_path = path
    if not path.endswith("delete.png"):
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
        no_padding_objects = ["Object_Tree", "Object_Rock_Stone", "Object_Rock_Dirt", "Object_Wood_Log", "Object_Tree_Bush", "Object_Tree_2", "Object_Woord_Log_2", "Object_Wood_Log_3", "Object_Mud", "Object_Mud_2", "Object_Water"]
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
    for o in overlays:
        draw_overlay(o["path"], o["row"], o["col"])

def change_map():
    global tk_bg_img, bg_img, canvas_w, canvas_h, canvas, cell_w, cell_h, GRID_ROWS, GRID_COLS, overlays
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

    overlays.clear()

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

root = tk.Tk()
root.title("Digital Dungeons-And-Dragons")
root.configure(bg="#222222")
root.attributes("-fullscreen", True)

bg_img = Image.open(BACKGROUND_IMAGE)
img_width, img_height = bg_img.size
screen_w, screen_h = root.winfo_screenwidth(), root.winfo_screenheight()
max_w, max_h = int(screen_w * 0.9), int(screen_h * 0.9)
scale = min(max_w / img_width, max_h / img_height, 1.0)

canvas_w = int(img_width * scale)
canvas_h = int(img_height * scale)
resized_bg = bg_img.resize((canvas_w, canvas_h), Image.LANCZOS)
tk_bg_img = ImageTk.PhotoImage(resized_bg)

main_frame = tk.Frame(root, bg="#222222")
main_frame.pack(fill="both", expand=True)

left_panel = tk.Frame(main_frame, bg="#222222")
left_panel.pack(side="left", fill="y", padx=10, pady=10)

top_controls = tk.Frame(main_frame, bg="#222222")
top_controls.pack(side="top", anchor="ne", padx=10, pady=5)

tk.Label(top_controls, text="Zeilen:", bg="#222222", fg="white").pack(side="left", padx=(0, 5))

entry_rows = tk.Entry(top_controls, width=4, bg="#333333", fg="white", insertbackground="white",
                      relief="flat", highlightthickness=1, highlightbackground="#555", highlightcolor="#777")
entry_rows.insert(0, str(GRID_ROWS))
entry_rows.pack(side="left", padx=(0, 10))

tk.Label(top_controls, text="Spalten:", bg="#222222", fg="white").pack(side="left", padx=(0, 5))

entry_cols = tk.Entry(top_controls, width=4, bg="#333333", fg="white", insertbackground="white",
                      relief="flat", highlightthickness=1, highlightbackground="#555", highlightcolor="#777")
entry_cols.insert(0, str(GRID_COLS))
entry_cols.pack(side="left", padx=(0, 10))

btn_map = tk.Button(
    top_controls,
    text="Change Map",
    command=change_map,
    bg="#444444",
    fg="white",
    activebackground="#555555",
    relief="flat",
    borderwidth=0,
    highlightthickness=0,
    padx=10,
    pady=5,
    font=("Arial", 10, "bold")
)
btn_map.pack(side="left")

btn_map.bind("<Enter>", lambda e: e.widget.config(bg="#555555"))
btn_map.bind("<Leave>", lambda e: e.widget.config(bg="#444444"))

canvas_frame = tk.Frame(main_frame, bg="#222222")
canvas_frame.pack(side="right", expand=True)

canvas = tk.Canvas(canvas_frame, width=canvas_w, height=canvas_h, bg="#222222", highlightthickness=0)
canvas.pack()

canvas.create_image(0, 0, anchor="nw", image=tk_bg_img)
cell_w = canvas_w / GRID_COLS
cell_h = canvas_h / GRID_ROWS

tooltip = tk.Label(root, text="", bg="#222222", fg="white", relief="solid", borderwidth=1,
                   font=("Arial", 10), padx=4, pady=2)
tooltip.place_forget()

def on_mouse_move(event):
    items = canvas.find_overlapping(event.x, event.y, event.x, event.y)
    for item in items:
        tag = canvas.gettags(item)
        if tag and tag[0].startswith("icon_"):
            icon_name = tag[0][5:]
            tooltip.config(text=icon_name)
            tooltip.place(x=event.x_root + 15, y=event.y_root + 10)
            return
    tooltip.place_forget()

canvas.bind("<Motion>", on_mouse_move)

MAX_ICONS_PER_ROW = 12

for category, icons in ICON_CATEGORIES.items():
    label = tk.Label(left_panel, text=category, font=("Arial", 12, "bold"), bg="#222222", fg="white")
    label.pack(anchor="w", pady=(10, 0))

    btn_frame = tk.Frame(left_panel, bg="#222222")
    btn_frame.pack(anchor="w", pady=5)

    for i, path in enumerate(icons):
        try:
            img = Image.open(path)
            img.thumbnail((60, 60))
            tk_icon = ImageTk.PhotoImage(img)
        except Exception as e:
            print(f"Fehler beim Laden von {path}: {e}")
            continue

        btn = tk.Button(btn_frame, image=tk_icon, command=lambda p=path: select_icon(p),
                        bg="#333333", activebackground="#555555", borderwidth=0)
        btn.image = tk_icon
        row = i // MAX_ICONS_PER_ROW
        col = i % MAX_ICONS_PER_ROW
        btn.grid(row=row, column=col, padx=3, pady=3)

        def make_tooltip(p):
            return lambda e: tooltip_show(p, e)
        
        btn.bind("<Enter>", make_tooltip(path))
        btn.bind("<Leave>", lambda e: tooltip.place_forget())

        if os.path.basename(path) == "delete.png":
            delete_btn = btn

delete_btn.config(command=lambda: set_delete_mode(not delete_mode))

def tooltip_show(path, event):
    tooltip.config(text=os.path.basename(path))
    tooltip.place(x=event.widget.winfo_rootx() + 60, y=event.widget.winfo_rooty())

canvas.bind("<Button-1>", on_canvas_click)
canvas.bind("<Button-3>", on_canvas_right_click)

root.mainloop()
