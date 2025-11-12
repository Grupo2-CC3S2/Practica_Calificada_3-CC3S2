
Name_ENV?=env

.DEFAULT_GOAL := help

# Ruta de Python dentro del venv
ifeq ($(OS),Windows_NT)
    PYTHON := $(Name_ENV)/Scripts/python
else
    PYTHON := $(Name_ENV)/bin/python
endif


.PHONY: build run snapshot test env clean help tools verify clean-env display zip unzip 

help:
# Muestra los objetivos disponibles en el Makefile
	@echo "Objetivos disponibles:"
	@echo "  make run         - Despliega todo el proyecto"
	@echo "  make snapshot    - Genera una instantánea de las métricas actuales"
	@echo "  make display     - Despliega el dashboard de métricas con streamlit"
	@echo "  make fastapi     - Despliega el dashboard simple de métricas con fastapi"
	@echo "  make test        - Ejecuta las pruebas unitarias"
	@echo "  make env         - Crea el entorno virtual e instala dependencias"
	@echo "  make clean-env   - Elimina el entorno virtual"
	@echo "  make clean       - Limpia archivos temporales y cachés"

build:
# Construye el proyecto (entorno virtual y dependencias)
	@make env
	@echo "Proyecto construido correctamente."
	@echo "Desempaquetando el proyecto..."
	@make unzip

run:
	@echo "Extrayendo métricas del Proyecto"
	@make snapshot
	@make forecast
	@echo "Ejecución completa del sistema"
	@echo "Levantando dashboard con fastapi"
	@make fastapi & pid=$$!; sleep 15; kill $$pid
	@echo "Servidor FastAPI cerrado correctamente."
	@echo "Levantando dashboard simple con Streamlit..."
	@make display & pid=$$!; sleep 15; kill $$pid
	@echo "Ejecución correcta de todo el proyecto"
	@echo "Ejecutando pruebas unitarias"
	@make test

snapshot:
# Genera una instantánea de las métricas actuales
	@make verify PROJECT_TOKEN=$$PROJECT_TOKEN
	@echo "Extrayendo métricas del Projecto"
	@$(PYTHON) data/extract_metrics.py

display:
# Despliega el dashboard de métricas
	@echo "Iniciando el dashboard de métricas"
	@$(PYTHON) -m streamlit run dashboard/app_streamlit.py

fastapi:
# Despliega el dashboard con fastapi
	@echo "Iniciando respuesta JSON con fastapi"
	@$(PYTHON) -m uvicorn dashboard.app_fastapi:app --reload

forecast:
# Genera un forecast de los snapshot según su fecha
	@echo "Generando forecast"
	@$(PYTHON) dashboard/forecast.py

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

zip:
# Comprime el proyecto en un archivo zip con nombre según la fecha en formato YYYY-MM-DD y elimina las carpetas empaquetadas
# El nombre es la fecha en YYYY-MM-DD y un hash 256 bits generado a partir de la fecha actual ejemplo: zip_2024-06-15_abcd1234....zip
	@DATE=$$(date +%F); HASH=$$(echo -n $${DATE} | sha256sum | cut -d' ' -f1); zip -r dist/zip_$${DATE}_$${HASH}.zip dashboard/ data/ test/ -x "*__pycache__*" -x "*.pytest_cache*"
	@echo "Proyecto comprimido en proyecto_$${DATE}_$${HASH}.zip"
	@echo "Eliminando carpetas empaquetadas..."
	@rm -rf dashboard/ data/ test/
	@echo "Eliminando entorno virtual"
	@make clean-env

unzip:
# Descomprime el archivo zip más reciente en la carpeta raiz
	@LATEST_ZIP=$$(ls -t dist/zip_*.zip | head -1); unzip -o $$LATEST_ZIP
	@echo "Archivo $$LATEST_ZIP descomprimido en la carpeta raiz."

clean-env:
# Elimina el entorno virtual
	rm -rf $(Name_ENV)

clean:
# Limpia archivos temporales y cachés
	rm -rf __pycache__ */__pycache__ .pytest_cache
