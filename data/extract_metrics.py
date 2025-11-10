#!/usr/bin/env python3
"""
Lee métricas desde un archivo CSV exportado de GitHub Projects.
"""
import csv, json, datetime
from pathlib import Path

def main():
    Path("data/snapshots").mkdir(parents=True, exist_ok=True)
    output = f"data/snapshots/snapshot-{datetime.date.today()}.json"

    with open("data/projects.csv", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        data = []
        for row in reader:
            data.append({
                "issue_id": row.get("ID"),
                "title": row.get("Title"),
                "status": row.get("Status"),
                "estimate": row.get("Estimate"),
                "sprint": row.get("Sprint"),
                "blocked_time": row.get("Blocked time")
            })

    with open(output, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

    print(f"snapshot desde csv generado: {output} ({len(data)} filas)")

if __name__ == "__main__":
    main()
