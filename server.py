from fastapi import FastAPI
from pydantic import BaseModel
import time
import logs


from engine_gemma import predict as gemma_predict

app = FastAPI()

class PredictIn(BaseModel):
    input: str
    model: str = "gemma2:2b"

@app.post("/predict")
def predict(body: PredictIn):
    t0 = time.time()

    if body.model == "gemma2:2b":
        output_text = gemma_predict(body.input)
        provider = "gemma2:2b"
    else:
        output_text = "Modelo no soportado."
        provider = "none"

    ms = int((time.time() - t0) * 1000)
    return {
        "output": output_text,
        "meta": {"provider": provider, "latency_ms": ms}
    }