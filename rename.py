import os

def rename_files_in_directory(directory):
    for filename in os.listdir(directory):
        old_path = os.path.join(directory, filename)

        if not os.path.isfile(old_path):
            print(f"'{filename}' ist keine Datei, wird übersprungen.")
            continue

        parts = filename.rsplit(" - ", 2)
        if len(parts) != 3:
            print(f"Dateiname '{filename}' passt nicht zum erwarteten Muster.")
            continue

        _, mid, end_with_ext = parts
        name, ext = os.path.splitext(end_with_ext)
        new_base = f"NPCs_{mid}_{name}{ext}"
        new_path = os.path.join(directory, new_base)

        counter = 1
        while os.path.exists(new_path):
            name_with_counter = f"NPCs_{mid}_{name}_{counter}{ext}"
            new_path = os.path.join(directory, name_with_counter)
            counter += 1

        try:
            print(f"Renaming '{filename}' to '{os.path.basename(new_path)}'")
            os.rename(old_path, new_path)
        except Exception as e:
            print(f"Fehler beim Umbenennen von '{filename}': {e}")

if __name__ == "__main__":
    folder = input("Pfad zum Verzeichnis eingeben: ")
    rename_files_in_directory(folder)
