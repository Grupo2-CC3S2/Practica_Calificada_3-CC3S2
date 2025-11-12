import pytest
import json

@pytest.fixture
def sample_data(tmp_path):
    """
    Fixture que crea un dataset temporal simulado.
    """
    test_file = tmp_path / "test_cards.json"
    test_content = [
        {"id": 1, "lead_time": 3, "status": "done"},
        {"id": 2, "lead_time": 5, "status": "done"},
    ]
    with open(test_file, "w") as f:
        json.dump(test_content, f)
    return test_file
