#!/usr/bin/env python3
import json, datetime
import pandas as pd
from pathlib import Path

SNAPSHOT_DIR = Path("data/snapshots")
OUTPUT_FILE = Path("data/forecast-latest.json")

def load_snapshots():
    rows = []
    for file in sorted(SNAPSHOT_DIR.glob("snapshot-*.json")):
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

def calculate_velocity(df):
    done = df[df["status"].str.lower() == "done"]
    if done.empty:
        return 0
    daily = done.groupby("date")["estimate"].sum().reset_index()
    return daily["estimate"].mean()

def estimate_completion(df, velocity):
    total = df["estimate"].sum()
    done = df[df["status"].str.lower() == "done"]["estimate"].sum()
    remaining = total - done
    if velocity <= 0:
        return None
    days_needed = remaining / velocity
    forecast_date = datetime.date.today() + datetime.timedelta(days=round(days_needed))
    return {
        "today": str(datetime.date.today()),
        "total_points": total,
        "done_points": done,
        "remaining_points": remaining,
        "velocity": round(velocity, 2),
        "days_needed": round(days_needed, 1),
        "forecast_date": str(forecast_date)
    }

def main():
    df = load_snapshots()
    velocity = calculate_velocity(df)
    result = estimate_completion(df, velocity)
    if result:
        with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
            json.dump(result, f, indent=2)
        print("Forecast generado:", result)
    else:
        print("No se pudo calcular el forecast (velocity=0)")

if __name__ == "__main__":
    main()
