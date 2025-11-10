Crear token clasico desde https://github.com/settings/tokens

Crearlo con el nombre: **PROJECT_TOKEN**
Darle acceso a:
    repo
    repo:org
    read:project

Guardar el TOKEN

Ejecutar:
```bash
export PROJECT_TOKEN=ghp_tuTokenAqui
```
Y luego
```bash
python extract_metrics.py"
```