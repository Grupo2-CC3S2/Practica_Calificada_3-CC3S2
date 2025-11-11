
Name_ENV?=env

.DEFAULT_GOAL := help

# Ruta de Python dentro del venv
ifeq ($(OS),Windows_NT)
    PYTHON := $(Name_ENV)/Scripts/python
else
    PYTHON := $(Name_ENV)/bin/python
endif


.PHONY: run snapshot test env clean help tools verify clean-env display

help:
# Muestra los objetivos disponibles en el Makefile
	@echo "Objetivos disponibles:"
	@echo "  make run         - Despliega todo el proyecto"
	@echo "  make snapshot    - Genera una instantánea de las métricas actuales"
	@echo "  make display     - Despliega el dashboard de métricas"
	@echo "  make test        - Ejecuta las pruebas unitarias"
	@echo "  make env         - Crea el entorno virtual e instala dependencias"
	@echo "  make clean-env   - Elimina el entorno virtual"
	@echo "  make clean       - Limpia archivos temporales y cachés"

run:
	@echo "Extrayendo métricas del Proyecto"
	@$(PYTHON) data/extract_metrics.py

snapshot:
# Genera una instantánea de las métricas actuales
	@make verify
	@echo "Extrayendo métricas del Projecto"
	@$(PYTHON) data/extract_metrics.py

display:
# Despliega el dashboard de métricas
	@echo "Iniciando el dashboard de métricas"
	@$(PYTHON) -m streamlit run dashboard/app_streamlit.py

test:
# Ejecuta las pruebas unitarias con pytest
	@$(PYTHON) -m pytest -vv --tb=short

env:
# Creación del entorno virtual e instalación de dependencias
	@python -m venv $(Name_ENV)
	@echo "Entorno virtual creado en el directorio '$(Name_ENV)'."
	@make tools
	@echo "Para activarlo, use el siguiente comando:"
	@echo "source $(Name_ENV)/Scripts/activate"

tools:
# Instalación de dependencias en el entorno virtual
	@$(PYTHON) -m pip install -r requirements.txt
	@echo "Dependencias instaladas en el entorno virtual."

verify:
# Verificación de activación del entorno virtual
	@if [ ! -d "$(Name_ENV)" ]; then \
		echo "Error: El entorno virtual no ha sido creado. Por favor, ejecute 'make env' primero."; \
		exit 1; \
	fi
	@echo "El entorno virtual ha sido creado."
# Verifica la creación de la variable de entorno PROJECT_TOKEN
	@if [ -z "$$PROJECT_TOKEN" ]; then \
		echo "Error: PROJECT_TOKEN no ha sido definido. Por favor, defínelo antes de ejecutar este objetivo."; \
		echo "Ejemplo: export PROJECT_TOKEN=<valor_token>"; \
		exit 1; \
	fi
	@echo "PROJECT_TOKEN está definido."

clean-env:
# Elimina el entorno virtual
	rm -rf $(Name_ENV)

clean:
# Limpia archivos temporales y cachés
	rm -rf __pycache__ */__pycache__ .pytest_cache
