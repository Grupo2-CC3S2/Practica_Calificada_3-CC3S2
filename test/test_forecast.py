import json
import pandas as pd
from dashboard.forecast import generate_forecast

def test_generate_forecast_basic(tmp_path):
    df = pd.DataFrame([
        {"status": "Done", "estimate": 5},
        {"status": "In Progress", "estimate": 3}
    ])
    date = pd.Timestamp("2025-11-01")

    forecast = generate_forecast(df, date)

    # Verificando campos del forecast
    assert "velocity" in forecast
    assert forecast["total_points"] == 8.0
    assert forecast["done_points"] == 5.0
    assert forecast["remaining_points"] == 3.0
    assert isinstance(forecast["alerts"], list)
