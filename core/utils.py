

import re
from typing import List, Tuple

def split_sentences(text: str) -> List[str]:
    sentences = re.split(r'(?<=[.!?])\s+', text.strip())
    return [s.strip() for s in sentences if s.strip()]

def find_urls(text: str) -> List[str]:
    url_re = re.compile(r'(https?://[^\s]+)|(www\.[^\s]+)', re.IGNORECASE)
    return [m.group(0) for m in url_re.finditer(text)]

def extract_claims(text: str) -> List[str]:
    return split_sentences(text)

def mark_spans(text: str, substrings: List[str]) -> List[Tuple[int,int,str]]:
    spans = []
    for sub in substrings:
        start = text.find(sub)
        if start >= 0:
            spans.append((start, start+len(sub), sub))
    return spans
