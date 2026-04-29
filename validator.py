import json
import re
from logs import LOGGER

ALLOWED_ACTIONS = ["saludar", "despedirse", "consultar_clima", "obtener_ayuda", "desconocido"]

def clean_markdown(raw: str) -> str:
    """Elimina bloques de código markdown si existen."""
    match = re.search(r"```(?:json)?\s*([\s\S]*?)\s*```", raw)
    if match:
        return match.group(1).strip()
    return raw.strip()

def validate_output(raw: str):
    """Devuelve (ok: bool, result: dict, error: str|None)."""
    try:
        clean_raw = clean_markdown(raw)
        obj = json.loads(clean_raw)
    except Exception as e:
        err_msg = f"json_parse_error: {e}"
        LOGGER.warning(err_msg)
        return False, None, err_msg

    # 1) estructura base
    if not isinstance(obj, dict):
        LOGGER.warning("not_a_dict")
        return False, None, "not_a_dict"

    if "ok" not in obj or "data" not in obj:
        LOGGER.warning("missing_ok_or_data")
        return False, None, "missing_ok_or_data"

    if not isinstance(obj["ok"], bool):
        LOGGER.warning("ok_not_bool")
        return False, None, "ok_not_bool"

    data = obj["data"]
    if not isinstance(data, dict):
        return False, None, "data_not_dict"

    # 2) claves obligatorias
    required = ["answer", "confidence", "actions", "error"]
    for k in required:
        if k not in data:
            LOGGER.warning(f"missing_field:{k}")
            return False, None, f"missing_field:{k}"

    # 3) tipos
    if not isinstance(data["answer"], str):
        LOGGER.warning("answer_not_str")
        return False, None, "answer_not_str"

    conf = data["confidence"]
    if not isinstance(conf, (int, float)):
        LOGGER.warning("confidence_not_number")
        return False, None, "confidence_not_number"
    if conf < 0 or conf > 1:
        LOGGER.warning("confidence_out_of_range")
        return False, None, "confidence_out_of_range"

    if not isinstance(data["actions"], list) or not all(isinstance(x, str) for x in data["actions"]):
        LOGGER.warning("actions_not_list_of_str")
        return False, None, "actions_not_list_of_str"
    
    # Validar contra catálogo
    for action in data["actions"]:
        if action not in ALLOWED_ACTIONS:
            LOGGER.warning(f"invalid_action:{action}")
            return False, None, f"invalid_action:{action}"

    if data["error"] is not None and not isinstance(data["error"], str):
        LOGGER.warning("error_not_str_or_null")
        return False, None, "error_not_str_or_null"

    # 4) Consistencia lógica (Rúbrica)
    if obj["ok"] is False and not data["error"]:
        LOGGER.warning("logic_error: ok_is_false_but_error_is_empty")
        return False, None, "logic_error: missing_error_message"

    return True, obj, None