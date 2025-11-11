from fastapi import FastAPI
from dashboard.metrics import load_snapshots, throughput, wip, velocity, cycle_time, slip_rate

app = FastAPI(title="Scrum Metrics API")

@app.get("/")
def read_root():
    df = load_snapshots()
    return {
        "total_items": len(df),
        "throughput": throughput(df),
        "wip": wip(df),
        "velocity": velocity(df),
        "cycle_time": float(cycle_time(df)) if cycle_time(df) else None,
        "slip_rate": slip_rate(df),
    }

@app.get("/data")
def get_raw_data():
    """Devuelve los datos crudos del snapshot"""
    df = load_snapshots()
    return df.to_dict(orient="records")

# Ejecucion
# uvicorn dashboard.app_fastapi:app --reload
# En la raiz del proyecto