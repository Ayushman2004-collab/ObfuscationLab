import base64
from app.core.encoders import encode_base64, encode_rot13, encode_xor_hex

def test_base64_representation():
    assert base64.b64decode(encode_base64("hello")).decode() == "hello"

def test_rot13_is_reversible():
    assert encode_rot13(encode_rot13("hello")) == "hello"

def test_xor_hex_is_hex():
    value = encode_xor_hex("hello", "key")
    assert value and all(c in "0123456789abcdef" for c in value)
