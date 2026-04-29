import logging
import os
import uuid
import sys

# Configuración del Logger
MODE = os.getenv("MODE", "dev")
level = logging.DEBUG if MODE == "dev" else logging.INFO

# Limpiar handlers previos para evitar duplicados en Uvicorn
for handler in logging.root.handlers[:]:
    logging.root.removeHandler(handler)

logging.basicConfig(
    level=level,
    format="%(asctime)s | %(levelname)-7s | %(name)s | %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)

# Silenciar loggers internos demasiado ruidosos
logging.getLogger("asyncio").setLevel(logging.WARNING)
logging.getLogger("httpcore").setLevel(logging.WARNING)
logging.getLogger("httpx").setLevel(logging.WARNING)
logging.getLogger("urllib3").setLevel(logging.WARNING)

LOGGER = logging.getLogger("validator")
LOGGER.setLevel(level)

def new_request_id():
    return str(uuid.uuid4())[:8]

def clip(s: str, n: int = 200) -> str:
    # Reemplazamos saltos de línea para que el log quede en una sola línea
    s = s.replace("\n", " ").replace("\r", "")
    return s if len(s) <= n else s[:n] + "…"
