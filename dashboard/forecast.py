#!/usr/bin/env python3
import json, datetime
import pandas as pd
from pathlib import Path

SNAPSHOT_DIR = Path("data/snapshots")
OUTPUT_FILE = Path("data/forecast/forecast-latest.json")

def load_snapshot(file):
    """Carga un snapshot individual y devuelve un DataFrame + fecha."""
    try:
        date = datetime.date.fromisoformat(file.stem.replace("snapshot-", ""))
    except ValueError:
        return None, None

    with open(file, encoding="utf-8") as f:
        data = json.load(f)

    df = pd.DataFrame(data)
    df["date"] = date
    return date, df


def calculate_velocity(df):
    """Velocidad = suma de estimaciones completadas (status Done)."""
    done = df[df["status"].str.lower() == "done"]
    return done["estimate"].sum() if not done.empty else 0


def generate_forecast(df, date):
    """Genera predicción por snapshot (día)."""
    velocity = calculate_velocity(df)
    total = df["estimate"].sum()
    done = df[df["status"].str.lower() == "done"]["estimate"].sum()
    remaining = total - done

    if velocity <= 0:
        forecast_date = "Indeterminado"
        days_needed = 0
    else:
        days_needed = remaining / velocity
        forecast_date = str(date + datetime.timedelta(days=round(days_needed)))

    alerts = []
    if velocity < 2:
        alerts.append("Velocidad baja (<2 pts)")
    if remaining > 2 * velocity:
        alerts.append("🚨 Posible sobrecarga del sprint")
    if not alerts:
        alerts.append("Sin alertas")

    return {
        "snapshot_date": str(date),
        "total_points": float(round(total, 2)),
        "done_points": float(round(done, 2)),
        "remaining_points": float(round(remaining, 2)),
        "velocity": float(round(velocity, 2)),
        "days_needed": float(round(days_needed, 1)),
        "forecast_date": forecast_date,
        "alerts": alerts
    }



def main():
    forecasts = []
    for file in sorted(SNAPSHOT_DIR.glob("snapshot-*.json")):
        date, df = load_snapshot(file)
        if df is None or df.empty:
            continue
        forecast = generate_forecast(df, date)
        forecasts.append(forecast)
        print(f"\n===========Forecast para {date}:===========")
        print(json.dumps(forecast, indent=2, ensure_ascii=False))

    if not forecasts:
        print("===========No hay snapshots válidos para procesar===========")
        return

    OUTPUT_FILE.parent.mkdir(exist_ok=True)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(forecasts, f, indent=2, ensure_ascii=False)

    print(f"\n===========Archivo generado: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
