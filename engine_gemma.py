import requests
import json
from validator import validate_output, clean_markdown
from logs import LOGGER, new_request_id, clip

OLLAMA_CHAT_URL = "http://localhost:11434/api/chat"
MODEL_NAME = "gemma2:2b"

SYSTEM_PROMPT = """
Eres un sistema de inteligencia artificial especializado en devolver ÚNICAMENTE datos en formato JSON.
Tu salida debe ser EXCLUSIVAMENTE un JSON válido, sin preámbulos, explicaciones ni texto adicional antes o después del bloque.

ESQUEMA OBLIGATORIO:
{
  "ok": boolean,
  "data": {
    "answer": "string",
    "confidence": number (0..1),
    "actions": ["string"],
    "error": "string" o null
  }
}

REGLAS CRÍTICAS:
1. IDIOMA: Responde siempre en español.
2. CONCISIÓN: La respuesta ('answer') debe ser directa, útil y no superar las 20 palabras.
3. SEGURIDAD: Ante insultos, contenido ofensivo o peticiones peligrosas, responde con ok=false y error="Contenido no permitido".
4. ACCIONES: Utiliza solo este catálogo: [saludar, despedirse, consultar_clima, obtener_ayuda, desconocido].
5. FORMATO: Escapa comillas dobles en strings. El valor null no lleva comillas.
6. PERSONA: Identifícate como "Asistente IA".

ESTADO:
- Éxito: ok=true, error=null.
- Fallo: ok=false, answer="", confidence=0, actions=[], error="motivo".
"""

def predict(text: str, retry: bool = True) -> dict:
    rid = new_request_id()
    LOGGER.info(f"[{rid}] Nueva petición: {clip(text)}")
    
    payload = {
        "model": MODEL_NAME,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": text}
        ],
        "stream": False,
        "options": {
            "temperature": 0.0,
            "num_predict": 150,
            "stop": ["<start_of_turn>", "<end_of_turn>"]
        }
    }
    
    try:
        # Intento 1
        response = requests.post(OLLAMA_CHAT_URL, json=payload, timeout=120)
        response.raise_for_status()
        raw_content = response.json().get("message", {}).get("content", "").strip()
        LOGGER.debug(f"[{rid}] Raw response: {clip(raw_content)}")
        
        # Validar
        is_valid, obj, error = validate_output(raw_content)
        
        # Estrategia de reintento/reparación
        if not is_valid and retry:
            LOGGER.warning(f"[{rid}] Error de validación en intento 1: {error}. Reintentando reparación...")
            
            # Message de reparación mas explícito
            repair_message = (
                f"Tu respuesta anterior es INVÁLIDA: {error}. "
                "REGLA CRÍTICA: Si 'ok' es false, el campo 'error' DEBE contener un mensaje de texto con el motivo. "
                "Por favor, devuelve el JSON corregido ahora."
            )
            
            # Añadimos el historial para el reintento
            payload["messages"].append({"role": "assistant", "content": raw_content})
            payload["messages"].append({"role": "user", "content": repair_message})
            
            # Intento 2
            response = requests.post(OLLAMA_CHAT_URL, json=payload, timeout=120)
            response.raise_for_status()
            raw_content = response.json().get("message", {}).get("content", "").strip()
            is_valid, obj, error = validate_output(raw_content)

        if not is_valid:
            LOGGER.error(f"[{rid}] Fallo definitivo tras reintento: {error}")
            return {
                "ok": False,
                "data": {"answer": "", "confidence": 0, "actions": [], "error": f"error: {error}"},
                "raw": raw_content
            }
        
        LOGGER.info(f"[{rid}] Respuesta válida generada.")
        return obj
            
    except Exception as e:
        LOGGER.error(f"[{rid}] Error del sistema en predict: {e}")
        return {
            "ok": False,
            "data": {"answer": "", "confidence": 0, "actions": [], "error": f"system_error: {e}"}
        }
