# Practica 10 - FastAPI + Gradio
## Instalación

```bash
python -m pip install -r requeriments.txt
```

## Ejecución

```bash
uvicorn server:app --host [IP_ADDRESS] --port 8000 --reload
python app.py
```

## Evidencia de mejora

Al implementar la estrategia de reparación (reintentos automáticos), el sistema es capaz de corregir errores de formato JSON en tiempo real, aumentando significativamente la tasa de éxito.

| Con reintento? | Total Pruebas | Tenian que fallar |Válidos | Fallidos | Precisión | Errores encontrados                                                   |
| :------------- | :------------ |:----------------- |:------ | :------- | :-------- | :-------------------------------------------------------------------- |
| No             | 10            |2                  |8       | 2        | 80.0%     | json_parse_error, missing_field                                       |
| **Sí**         | 10            |2                  |8       | 0        | **100.0%** | Contenido no permitido y la entrada debe contener información valida. |
