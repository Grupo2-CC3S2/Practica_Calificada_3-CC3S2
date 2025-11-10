#!/usr/bin/env python3
"""
extract_metrics.py (versión simple Día 1)
Simula la recolección de métricas Scrum y guarda un snapshot JSON local.
"""
import json, datetime
from pathlib import Path

def main():
    fake_items = [
        {"issue_id": 1, "title": "Configurar entorno", "status": "In Progress", "estimate": 3, "sprint": "Sprint 1", "blocked_time": 0},
        {"issue_id": 2, "title": "Diseñar tablero", "status": "Done", "estimate": 5, "sprint": "Sprint 1", "blocked_time": 1},
        {"issue_id": 3, "title": "Prueba extractor", "status": "To Do", "estimate": 2, "sprint": "Sprint 1", "blocked_time": 0},
    ]

    Path("data/snapshots").mkdir(parents=True, exist_ok=True)
    filename = f"data/snapshots/snapshot-{datetime.date.today()}.json"

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(fake_items, f, indent=2)

    print(f"Snapshot local generado: {filename} ({len(fake_items)} items)")

if __name__ == "__main__":
    main()
