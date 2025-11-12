#!/usr/bin/env python3

import json
import datetime
from pathlib import Path

def main():
    Path("data").mkdir(exist_ok=True)
    result = {
        "today": str(datetime.date.today()),
        "total_points": 20,
        "done_points": 10,
        "remaining_points": 10,
        "velocity": 3.3,
        "days_needed": 3,
        "forecast_date": str(datetime.date.today() + datetime.timedelta(days=3))
    }

    with open("data/forecast-latest.json", "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2)
    print("Forecast simulado generado:", result)

if __name__ == "__main__":
    main()
