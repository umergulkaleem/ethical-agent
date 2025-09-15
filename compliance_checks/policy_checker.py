# compliance_checks/policy_checker.py
import json, re
from typing import Dict, Any
from core.aiml_client import chat_completion

POLICY_PROMPT = """
You are a policy compliance assistant. Given this text, check if it violates any policies.
Policies include:
- no medical advice
- no legal advice
- no personal sensitive data

Return JSON:
{ "violations": [ { "policy_id": str, "explanation": str, "severity": "low|medium|high" } ] }

Text:
\"\"\"{text}\"\"\" 
"""

def check_policies(text: str) -> Dict[str, Any]:
    try:
        raw = chat_completion(POLICY_PROMPT.format(text=text))
        m = re.search(r'(\{.*\})', raw, re.S)
        payload = raw if not m else m.group(1)
        parsed = json.loads(payload)
        parsed.setdefault("raw", raw)
        return {"check": "policy", "engine": "aiml-gpt", **parsed}
    except Exception as e:
        return {"check": "policy", "engine": "rules", "violations": [], "error": str(e)}
