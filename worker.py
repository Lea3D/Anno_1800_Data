import json
import os
import glob

# Basisverzeichnis (Root) und Pfade definieren
root_dir = os.getcwd()  # Annahme: Skript wird im Root ausgeführt
data_dir = os.path.join(root_dir, "data")
guids_file = os.path.join(root_dir, "guids.json")

# 1. guids.json laden und Mapping erstellen: guid (Zahl) -> id (String)
with open(guids_file, "r", encoding="utf-8") as f:
    guids_data = json.load(f)

guid_to_id = {}
for entry in guids_data:
    if "guid" in entry and "id" in entry:
        guid_to_id[entry["guid"]] = entry["id"]

# 2. Alle JSON-Dateien im Ordner data verarbeiten
for file_path in glob.glob(os.path.join(data_dir, "*.json")):
    with open(file_path, "r", encoding="utf-8") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError as e:
            print(f"Fehler beim Laden von {file_path}: {e}")
            continue

    changed = False
    # Handhabung unterschiedlicher Datenstrukturen (Liste oder Dictionary)
    if isinstance(data, list):
        items = data
    elif isinstance(data, dict):
        items = list(data.values())
    else:
        print(f"Unbekannte Datenstruktur in {file_path}")
        continue

    # Iteriere durch alle Blöcke
    for record in items:
        if isinstance(record, dict) and "factories" in record:
            factories = record.get("factories")
            if isinstance(factories, list):
                new_factories = []
                for factory_guid in factories:
                    if factory_guid in guid_to_id:
                        new_factories.append(guid_to_id[factory_guid])
                        changed = True
                    else:
                        new_factories.append(factory_guid)
                        print(f"Warning: Factory-GUID {factory_guid} in {file_path} nicht im Mapping gefunden.")
                record["factories"] = new_factories

    # Speichere nur, wenn Änderungen vorgenommen wurden
    if changed:
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"Datei aktualisiert: {file_path}")
    else:
        print(f"In {file_path} wurden keine Änderungen vorgenommen.")

print("Verarbeitung aller Dateien abgeschlossen.")
