#!/usr/bin/env python3
import json, datetime
import pandas as pd
from pathlib import Path

SNAPSHOT_DIR = Path("data/snapshots")
OUTPUT_FILE = Path("data/forecast-latest.json")

def load_snapshots():
    rows = []
    for file in sorted(SNAPSHOT_DIR.glob("snapshot-*.json")):
        try:
            date = datetime.date.fromisoformat(file.stem.replace("snapshot-", ""))
        except ValueError:
            continue
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

def generate_forecast(df):
    velocity = calculate_velocity(df)
    total = df["estimate"].sum()
    done = df[df["status"].str.lower() == "done"]["estimate"].sum()
    remaining = total - done
    if velocity <= 0:
        forecast_date = "Indeterminado"
        days_needed = 0
    else:
        days_needed = remaining / velocity
        forecast_date = str(datetime.date.today() + datetime.timedelta(days=round(days_needed)))

    # alertas
    alerts = []
    if velocity < 2:
        alerts.append("Velocidad baja (<2 pts/día)")
    if remaining > 2 * velocity:
        alerts.append("🚨 Posible sobrecarga de sprint")
    if not alerts:
        alerts.append("Sin alertas")

    return {
        "today": str(datetime.date.today()),
        "total_points": round(total, 2),
        "done_points": round(done, 2),
        "remaining_points": round(remaining, 2),
        "velocity": round(velocity, 2),
        "days_needed": round(days_needed, 1),
        "forecast_date": forecast_date,
        "alerts": alerts
    }

def main():
    df = load_snapshots()
    if df.empty:
        print("No hay snapshots disponibles.")
        return
    forecast = generate_forecast(df)
    OUTPUT_FILE.parent.mkdir(exist_ok=True)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(forecast, f, indent=2, ensure_ascii=False)
    print("Forecast final generado:")
    print(json.dumps(forecast, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()
