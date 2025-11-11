# dashboard/metrics.py
import pandas as pd
from pathlib import Path
import json

def load_snapshots(path="data/snapshots"):
    data = []
    for file in Path(path).glob("snapshot-*.json"):
        with open(file, "r", encoding="utf-8") as f:
            data.extend(json.load(f))
    return pd.DataFrame(data)

def throughput(df):
    return len(df[df["status"] == "Done"])

def wip(df):
    return len(df[df["status"] == "In Progress"])

def velocity(df):
    return df[df["status"] == "Done"]["estimate"].sum()

def cycle_time(df):
    # aquí podrías calcular algo más realista si tienes fechas
    return df["blocked_time_(hrs)"].mean() if "blocked_time_(hrs)" in df else None

def slip_rate(df):
    done = df[df["status"] == "Done"]
    return 1 - len(done) / len(df) if len(df) > 0 else 0
