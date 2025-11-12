# Practica_Calificada_3-CC3S2
Proyecto 6 - Observabilidad de Scrum: métricas, insights y forecast

## Integrantes
- Yorklin Lazaro
- Christian Luna

# Sprint 1
Para el sprint 1 nos encargamos de realizar el Proyecto Kanban base con los campos **block_time** en **hrs**, **estimate** y **Sprint**, para agregarlos de acuerdo a los Issues que creemos para el sprint, luego de tener listo nuestro Proyecto Kanban, pasamos a crear el script [extract_metrics.py](data/extract_metrics.py) base el cual tenía como entrada un Dataframe falso con issues creados para realizar un snapshot en formato JSON para guardar las métricas de estos fake issues.

# Sprint 2
Para el sprint 2 mejoramos el script [extrac_metrics.py](data/extract_metrics.py) para que recolecte issues del Proyecto Kanban creado, esto se logró implementando la API de Github Projects además de generar un **secret** en el repositorio el cual nos dará acceso a este proyecto y así poder realizar tanto el pipeline como las pruebas. Además se crearon los archivos [app_streamlit.py](dashboard/app_streamlit.py) y [app_fastapi.py](dashboard/app_fastapi.py) el cual tiene como función levantar una interfaz web para que permita la visualización de estos [snapshots](data/snapshots/snapshot-2025-11-12.json) recolectados y así poder tener un dashboard que permita una mejor legibilidad, primero se hizo una interfaz con fastapi pero al ser muy simple se optó por usar streamlit para generar una interfaz más dinámica y entendible, por último se crearon las pruebas [test_extractor.py](test/test_extractor.py) el cual generaba pruebas unitarias para el script extract_metrics.py haciendo uno de parametrize, y fixtures para casos diverso.

# Sprint 3
Para el sprint 3 se creó el script [forecast.py](dashboard/forecast.py) el cual nos genera un forecast de acuerdo a las métricas recolectadas en los snapshots, de manera que nos muestre un resumen de velocidad, tareas en Done, tareas en In Progrees, y distintas características solicitadas por las rúbricas, además de implementar por completo nuestro [Makefile](Makefile) el cual ya posee tareas robustas para automatizar todo el despliegue del proyecto sin necesidad de repetir código.