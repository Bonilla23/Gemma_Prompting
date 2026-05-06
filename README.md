# Practica 10 - FastAPI + Gradio

## Instalación
```bash
python -m pip install -r requeriments.txt
```

## Ejecución
Para iniciar el servidor (API):
```bash
uvicorn server:app --host 127.0.0.1 --port 8000 --reload
```

Para iniciar la interfaz (Gradio):
```bash
python app.py
```

## Evaluación (Tests)
Para ejecutar la suite de métricas y comprobar la precisión:
```bash
python run_eval.py
```

## Evidencia de mejora
Al implementar la estrategia de reparación (reintentos automáticos), el sistema es capaz de corregir errores de formato JSON en tiempo real, aumentando la tasa de éxito.

| Con reintento? | Total Pruebas | Válidos | Fallidos | Precisión | Errores comunes                                                      |
| :------------- | :------------ | :------ | :------- | :-------- | :------------------------------------------------------------------- |
| No             | 10            | 8       | 2        | 80.0%     | json_parse_error, missing_field                                      |
| **Sí**         | 10            | 9       | 1        | 90.0%     | En la pregunta del texto vacio, ha pensado que el texto estaba vacio |

---

## Archivos del Proyecto
* `server.py`: Servidor FastAPI (Endpoint `/predict`).
* `engine_gemma.py`: Lógica de IA y reintentos.
* `validator.py`: Validación de JSON.
* `run_eval.py`: Evaluación de métricas.
* `app.py`: Cliente Gradio.
* `logs.py`: Configuración de logs.
* `prompts.md`: Historial de prompts.
