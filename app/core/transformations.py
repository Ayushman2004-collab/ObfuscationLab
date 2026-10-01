import json

def split_join(text: str, chunk_size: int = 4) -> str:
    if not 1 <= int(chunk_size) <= 64:
        raise ValueError("chunk_size must be between 1 and 64.")
    chunks = [text[i:i + int(chunk_size)] for i in range(0, len(text), int(chunk_size))]
    return "|".join(chunks)

def unicode_escape_view(text: str) -> str:
    # A printable representation only; it is never evaluated or executed.
    return "".join(f"\\u{ord(char):04x}" if ord(char) <= 0xFFFF
                   else f"\\U{ord(char):08x}" for char in text)

def marker_insert(text: str, marker: str = "~") -> str:
    if len(marker) != 1 or marker.isalnum():
        raise ValueError("marker must be one non-alphanumeric character.")
    return marker.join(text)

def apply_transformation(text: str, name: str, params=None) -> str:
    params = params or {}
    if name == "split_join":
        return split_join(text, int(params.get("chunk_size", 4)))
    if name == "unicode_view":
        return unicode_escape_view(text)
    if name == "marker_view":
        return marker_insert(text, str(params.get("marker", "~")))
    raise ValueError(f"Unsupported transformation: {name}")

def normalize_pipeline(pipeline):
    if not isinstance(pipeline, list) or len(pipeline) > 8:
        raise ValueError("pipeline must be a list containing at most 8 steps.")
    normalized = []
    allowed = {
        "encoder": {"base64", "rot13", "xor_hex"},
        "transform": {"split_join", "unicode_view", "marker_view"},
    }
    for step in pipeline:
        if not isinstance(step, dict):
            raise ValueError("Each pipeline step must be an object.")
        kind, name = step.get("kind"), step.get("name")
        if kind not in allowed or name not in allowed[kind]:
            raise ValueError("Unsupported pipeline step.")
        params = step.get("params", {})
        if not isinstance(params, dict):
            raise ValueError("Step params must be an object.")
        normalized.append({"kind": kind, "name": name, "params": params})
    return normalized
