# Esquema JSON utilizado

```json
{
  "ok": true,
  "data": {
    "answer": "string",
    "confidence": 0.0,
    "actions": ["string"],
    "error": null
  }
}
```

## Ejemplo del uso del esquema

```json
{
  "ok": true,
  "data": {
    "answer": "Hola, ¿en qué puedo ayudarte?",
    "confidence": 0.9,
    "actions": ["saludar"],
    "error": null
  }
}
```

## Ejemplo de respuesta vacía

```json
{
  "ok": false,
  "data": {
    "answer": "",
    "confidence": 0.0,
    "actions": [],
    "error": "No se pudo obtener una respuesta."
  }
}
```
