import re
import math
from collections import Counter

# Synthetic strings exist only to demonstrate deterministic static matching.
LAB_RULES = {
    "LAB-001": {"description": "Synthetic alpha marker", "pattern": "LAB_TEST_MARKER_ALPHA"},
    "LAB-002": {"description": "Synthetic beta marker", "pattern": "LAB_TEST_MARKER_BETA"},
    "LAB-003": {"description": "Synthetic gamma marker", "pattern": "LAB_TEST_MARKER_GAMMA"},
}

def detect(text: str):
    matches = []
    for rule_id, rule in LAB_RULES.items():
        if rule["pattern"] in text:
            matches.append({"rule_id": rule_id, "description": rule["description"]})
    return {"detected": bool(matches), "matches": matches}

def shannon_entropy(text: str) -> float:
    if not text:
        return 0.0
    counts = Counter(text)
    length = len(text)
    return round(-sum((n / length) * math.log2(n / length) for n in counts.values()), 4)

def feature_summary(text: str):
    return {
        "length": len(text),
        "unique_character_ratio": round(len(set(text)) / max(len(text), 1), 4),
        "shannon_entropy": shannon_entropy(text),
        "contains_non_ascii": any(ord(ch) > 127 for ch in text),
    }
