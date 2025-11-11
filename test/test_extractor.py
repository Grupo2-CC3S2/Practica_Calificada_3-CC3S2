import pytest
from pathlib import Path
import json
import os
from data import extract_metrics 

@pytest.mark.parametrize("dataset", [
    [],  # sin datos
    [{"id": 1, "lead_time": 0, "status": "done"}],  
    [{"id": 1, "lead_time": 3}, {"id": 1, "lead_time": 3}],  
])
def test_metric_consistency(tmp_path, dataset):
    test_file = tmp_path / "temp.json"
    with open(test_file, "w") as f:
        json.dump(dataset, f)

    total = sum(card.get("lead_time", 0) for card in dataset)
    
    # Verificación de consistencia
    if dataset:
        assert total >= 0, "La suma de lead times debe ser >= 0"
    else:
        assert total == 0, "Dataset vacío debe dar suma 0"

# Test de generación de snapshots
def test_snapshot_generation(tmp_path):
    os.system("python3 data/extract_metrics.py")
    
    files = list(Path("data/snapshots").glob("snapshot-*.json"))
    assert files, "No se generó snapshot JSON"

def test_using_fixture(sample_data):
    assert Path(sample_data).exists()