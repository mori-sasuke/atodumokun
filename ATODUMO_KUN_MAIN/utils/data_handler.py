import json
import os

SAVE_PATH = "data/records.json"

def save_record(record):
    records = load_records()
    records.append(record)
    os.makedirs(os.path.dirname(SAVE_PATH), exist_ok=True)
    with open(SAVE_PATH, "w", encoding="utf-8") as f:
        json.dump(records, f, indent=2)

def load_records():
    if not os.path.exists(SAVE_PATH):
        return []
    with open(SAVE_PATH, "r", encoding="utf-8") as f:
        return json.load(f)
