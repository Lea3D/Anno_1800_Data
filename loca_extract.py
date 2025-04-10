import json
import glob
import os

# Quellverzeichnis und Backup-Verzeichnis definieren
source_dir = "params_sep"
backup_dir = "backup_files"
os.makedirs(backup_dir, exist_ok=True)

# Liste zum Sammeln der locaText-Daten
loca_texts = []

# Alle JSON-Dateien im Quellverzeichnis verarbeiten
for file_path in glob.glob(os.path.join(source_dir, "*.json")):
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    # Ermitteln, ob data ein Array oder ein Dictionary ist
    if isinstance(data, dict):
        modules = list(data.values())
    elif isinstance(data, list):
        modules = data
    else:
        print(f"Unbekannte Datenstruktur in {file_path}")
        continue

    # Iteriere über alle Module
    for module in modules:
        # Sicherstellen, dass es sich bei module um ein Dictionary handelt
        if isinstance(module, dict):
            extracted = {
                "guid": module.get("guid"),
                "name": module.get("name"),
                "locaText": module.get("locaText")
            }
            loca_texts.append(extracted)
            # Entferne den locaText-Block aus dem Modul
            module.pop("locaText", None)
        else:
            print(f"Überspringe nicht erwartetes Element: {module}")

    # Speichere eine Kopie als Backup
    backup_file = os.path.join(backup_dir, os.path.basename(file_path))
    with open(backup_file, "w", encoding="utf-8") as backup:
        json.dump(data, backup, indent=2, ensure_ascii=False)
    
    # Speichere die modifizierte Version in der Originaldatei
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

# Speichere alle extrahierten locaText-Daten in eine separate JSON-Datei
with open("loca_texts.json", "w", encoding="utf-8") as f:
    json.dump(loca_texts, f, indent=2, ensure_ascii=False)
