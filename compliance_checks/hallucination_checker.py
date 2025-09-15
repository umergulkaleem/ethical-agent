# compliance_checks/hallucination_checker.py
import json, re, time
from typing import Dict, Any
from core.utils import extract_claims, find_urls
from core.aiml_client import chat_completion

HALLUC_PROMPT = """
You are a fact-check assistant. Given the following sentence, respond in JSON with keys:
- claim: the sentence
- is_fact_like: true/false
- needs_source: true/false
- required_sources: suggested sources or search terms (array)
- explanation: short reasoning
Only output JSON.

Sentence:
\"\"\"{sentence}\"\"\" 
"""

def check_hallucinations(text: str) -> Dict[str, Any]:
    claims = extract_claims(text)
    issues = []
    urls = find_urls(text)

    for s in claims:
        try:
            raw = chat_completion(HALLUC_PROMPT.format(sentence=s))
            m = re.search(r'(\{.*\})', raw, re.S)
            payload = raw if not m else m.group(1)
            parsed = json.loads(payload)
            parsed["_raw"] = raw
            if parsed.get("needs_source") or parsed.get("is_fact_like"):
                issues.append({"sentence": s, "verdict": parsed})
        except Exception as e:
            issues.append({"sentence": s, "error": str(e)})

    return {
        "check": "hallucination",
        "urls_found": urls,
        "issues": issues,
        "summary": f"Analyzed {len(claims)} sentences",
        "checked_at": int(time.time()),
    }
