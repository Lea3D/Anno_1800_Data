import json
import csv
import os

# Pfade festlegen
input_file = "factories.json"     # Passe den Pfad an, falls nötig
output_file = "factories.csv"

# CSV-Spaltenüberschriften (im gewünschten Zielnamen)
csv_columns = [
    # Top-Level
    "can_clip",
    "dlcs",
    "fertilizer_module",
    "free_area",
    "friendly_name",
    "guid",
    "icon",
    "id",
    "module",
    "modules_limit",
    "modules_size",
    "palace_buff",
    "region",
    "set_buff",
    "tpmin",
    "shutdown_threshold",
    # Inputs (max. 3)
    "input_product_1_id",
    "input_product_1_amount",
    "input_product_1_storage_amount",
    "input_product_2_id",
    "input_product_2_amount",
    "input_product_2_storage_amount",
    "input_product_3_id",
    "input_product_3_amount",
    "input_product_3_storage_amount",
    # Maintenances
    "maintenance_cost_product",
    "maintenance_cost_amount",
    "maintenance_cost_inactive_amount",
    "workforce_product",
    "workforce_amount",
    "workforce_inactive_amount",
    # Outputs (max. 3)
    "output_product_1_id",
    "output_product_1_amount",
    "output_product_1_storage_amount",
    "output_product_2_id",
    "output_product_2_amount",
    "output_product_2_storage_amount",
    "output_product_3_id",
    "output_product_3_amount",
    "output_product_3_storage_amount",
    # Vector (optional)
    "vector_element",
    "inheritance_map",
    "entry",
    "index",
    "template_name"
]

def get_composite_value(record, composite_key):
    """
    Extrahiert rekursiv den Wert aus record anhand eines zusammengesetzten Schlüssels
    z.B. "inputs[0].Product" wird geparst.
    """
    if '[' not in composite_key:
        # Einfacher Top-Level-Zugriff
        return record.get(composite_key, "")
    else:
        # Zerlege: Beispiel "inputs[0].Product"
        try:
            top_key, remainder = composite_key.split('[', 1)  # z.B. top_key = "inputs", remainder = "0].Product"
            index_str, remainder = remainder.split(']', 1)    # index_str = "0", remainder = ".Product"
            index = int(index_str)
            remainder = remainder.lstrip('.')  # Entferne führende Punkte
            array = record.get(top_key, [])
            if not isinstance(array, list) or index >= len(array):
                return ""
            element = array[index]
            if remainder:
                return element.get(remainder, "")
            else:
                return element
        except Exception as e:
            return ""

def get_value(record, original_key):
    """
    Extrahiert den Wert für einen einfachen Top-Level-Schlüssel.
    """
    return record.get(original_key, "")

# Mapping-Liste: Original-Schlüssel -> Ziel-Spaltenname.
# Für Felder in Arrays nutzen wir das zusammengesetzte Format.
mapping = {
    # Top-Level
    "canClip": "can_clip",
    "dlcs": "dlcs",
    "fertilizerModule": "fertilizer_module",
    "freeArea": "free_area",
    "friendly_name": "friendly_name",
    "guid": "guid",
    "icon": "icon",
    "id": "id",
    "module": "module",
    "modulesLimit": "modules_limit",
    "modulesSize": "modules_size",
    "palaceBuff": "palace_buff",
    "region": "region",
    "setBuff": "set_buff",
    "tpmin": "tpmin",
    "ShutdownThreshold": "shutdown_threshold",
    # Inputs
    "inputs[0].Product": "input_product_1_id",
    "inputs[0].Amount": "input_product_1_amount",
    "inputs[0].StorageAmount": "input_product_1_storage_amount",
    "inputs[1].Product": "input_product_2_id",
    "inputs[1].Amount": "input_product_2_amount",
    "inputs[1].StorageAmount": "input_product_2_storage_amount",
    "inputs[2].Product": "input_product_3_id",
    "inputs[2].Amount": "input_product_3_amount",
    "inputs[2].StorageAmount": "input_product_3_storage_amount",
    # Maintenances – Gruppe 1 (maintenance_cost)
    "maintenances[0].Product": "maintenance_cost_product",
    "maintenances[0].Amount": "maintenance_cost_amount",
    "maintenances[0].InactiveAmount": "maintenance_cost_inactive_amount",
    # Maintenances – Gruppe 2 (workforce)
    "maintenances[1].Product": "workforce_product",
    "maintenances[1].Amount": "workforce_amount",
    "maintenances[1].InactiveAmount": "workforce_inactive_amount",
    # Outputs
    "outputs[0].Product": "output_product_1_id",
    "outputs[0].Amount": "output_product_1_amount",
    "outputs[0].StorageAmount": "output_product_1_storage_amount",
    "outputs[1].Product": "output_product_2_id",
    "outputs[1].Amount": "output_product_2_amount",
    "outputs[1].StorageAmount": "output_product_2_storage_amount",
    "outputs[2].Product": "output_product_3_id",
    "outputs[2].Amount": "output_product_3_amount",
    "outputs[2].StorageAmount": "output_product_3_storage_amount",
    # Vector (optional)
    "VectorElement": "vector_element",
    "InheritanceMapV2": "inheritance_map",
    "Entry": "entry",
    "Index": "index",
    "TemplateName": "template_name"
}

# Lade die JSON-Daten (erwarte, dass factories.json eine Liste von Objekten enthält)
if not os.path.exists(input_file):
    raise FileNotFoundError(f"Datei '{input_file}' nicht gefunden.")

with open(input_file, "r", encoding="utf-8") as f:
    factories = json.load(f)

# Erzeuge eine Liste der CSV-Zeilen (als Dictionary)
csv_rows = []

for record in factories:
    row = {}
    # Iteriere über alle mapping-Einträge
    for orig_key, target_key in mapping.items():
        # Wenn der Composite-Key kein Array-Zugriff beinhaltet, verwende get_value, ansonsten get_composite_value
        if '[' in orig_key:
            value = get_composite_value(record, orig_key)
        else:
            value = get_value(record, orig_key)
        # Falls der Wert eine Liste ist (z. B. dlcs) oder ein anderes Objekt, können wir es als JSON-String exportieren
        if isinstance(value, list) or isinstance(value, dict):
            try:
                value = json.dumps(value, ensure_ascii=False)
            except Exception:
                value = ""
        row[target_key] = value
    csv_rows.append(row)

# Schreibe die CSV-Datei
with open(output_file, "w", newline="", encoding="utf-8") as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=csv_columns, quoting=csv.QUOTE_ALL)
    writer.writeheader()
    for row in csv_rows:
        # Stelle sicher, dass alle Spalten vorhanden sind – falls nicht, setze leere Strings
        for col in csv_columns:
            if col not in row:
                row[col] = ""
        writer.writerow(row)

print(f"CSV-Datei '{output_file}' wurde erfolgreich erstellt.")
