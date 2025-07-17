# 履歴の保存・読込
import json
import os

DATA_PATH = "data/records.json"

def save_record(record):
    records = []
    if os.path.exists(DATA_PATH):
        with open(DATA_PATH, "r") as f:
            records = json.load(f)
    records.append(record)
    with open(DATA_PATH, "w") as f:
        json.dump(records, f, indent=2)

def load_records():
    if not os.path.exists(DATA_PATH):
        return []
    with open(DATA_PATH, "r") as f:
        return json.load(f)
