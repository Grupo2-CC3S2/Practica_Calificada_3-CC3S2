run:
	python3 data/extract_metrics.py

snapshot:
	python3 data/extract_metrics.py

test:
	pytest -vv --tb=short

env:
	python -m venv env
	source env/bin/activate
	pip install -r requirements.txt

clean:
	rm -rf __pycache__ */__pycache__ .pytest_cache
