#agregar test al makefile

from pathlib import Path
import os

def test_snapshot_generation():
    os.system("python3 data/extract_metrics.py")
    files = list(Path("data/snapshots").glob("snapshot-*.json"))
    assert files, "No se generó snapshot JSON"
