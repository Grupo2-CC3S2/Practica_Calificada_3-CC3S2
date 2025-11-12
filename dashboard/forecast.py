#!/usr/bin/env python3

import json, datetime
import pandas as pd
from pathlib import Path

SNAPSHOT_DIR = Path("data/snapshots")
OUTPUT_FILE = Path("data/forecast-latest.json")

def load_snapshots():
    rows = []
    for file in SNAPSHOT_DIR.glob("snapshot-*.json"):
        date = datetime.date.fromisoformat(file.stem.replace("snapshot-", ""))
        with open(file, encoding="utf-8") as f:
            data = json.load(f)
            for issue in data:
                rows.append({
                    "date": date,
                    "status": issue.get("status", ""),
                    "estimate": float(issue.get("estimate", 0) or 0)
                })
    return pd.DataFrame(rows)

def main():
    df = load_snapshots()
    total = df["estimate"].sum()
    done = df[df["status"].str.lower() == "done"]["estimate"].sum()
    remaining = total - done

    result = {
        "today": str(datetime.date.today()),
        "total_points": float(total),
        "done_points": float(done),
        "remaining_points": float(remaining)
    }

    OUTPUT_FILE.parent.mkdir(exist_ok=True)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2)
    print("Forecast parcial generado:", result)

if __name__ == "__main__":
    main()
