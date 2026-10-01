import base64
import codecs

def encode_base64(text: str) -> str:
    return base64.b64encode(text.encode("utf-8")).decode("ascii")

def encode_rot13(text: str) -> str:
    return codecs.encode(text, "rot_13")

def encode_xor_hex(text: str, key: str) -> str:
    if not key:
        raise ValueError("XOR key must not be empty.")
    raw = text.encode("utf-8")
    key_bytes = key.encode("utf-8")
    transformed = bytes(value ^ key_bytes[i % len(key_bytes)] for i, value in enumerate(raw))
    return transformed.hex()

def apply_encoder(text: str, name: str, params=None) -> str:
    params = params or {}
    if name == "base64":
        return encode_base64(text)
    if name == "rot13":
        return encode_rot13(text)
    if name == "xor_hex":
        return encode_xor_hex(text, str(params.get("key", "lab-key")))
    raise ValueError(f"Unsupported encoder: {name}")
