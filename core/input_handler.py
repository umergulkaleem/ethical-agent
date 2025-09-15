# core/input_handler.py
from typing import Any, Dict, Union
import json

def normalize_input(payload: Union[str, Dict, Any]) -> Dict:
    if isinstance(payload, dict):
        if 'text' in payload:
            return {'text': payload['text'], 'meta': payload.get('meta')}
        if 'output' in payload:
            return {'text': payload['output'], 'meta': payload.get('meta')}
        return {'text': json.dumps(payload), 'meta': None}
    if isinstance(payload, str):
        # attempt parse JSON
        try:
            parsed = json.loads(payload)
            return normalize_input(parsed)
        except Exception:
            return {'text': payload, 'meta': None}
    return {'text': str(payload), 'meta': None}
