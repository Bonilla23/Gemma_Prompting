import gradio as gr
import requests
import logs
from logs import LOGGER, clip

API_URL = "http://127.0.0.1:8000/predict"

def call_api(text, model):
    LOGGER.info(f"Llamando a la API [{model}]: {clip(text)}")
    payload = {
        "input": text,
        "model": model
    }
    try:
        r = requests.post(API_URL, json=payload, timeout=120)
        r.raise_for_status()
        res = r.json()
        LOGGER.info(f"Respuesta recibida: {clip(str(res))}")
        return res
    except Exception as e:
        LOGGER.error(f"Error en la llamada: {e}")
        return {"error": str(e)}

demo = gr.Interface(
    fn=call_api,
    inputs=[
        gr.Textbox(label="Input"),
        gr.Dropdown(choices=["gemma2:2b"], value="gemma2:2b", label="Modelo")
    ],
    outputs=gr.JSON(label="Response (Output + Meta)"),
    title="Cliente",
)

if __name__ == "__main__":
    demo.launch()