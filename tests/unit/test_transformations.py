import pytest
from app.core.transformations import split_join, unicode_escape_view, marker_insert

def test_split_join_output():
    assert split_join("abcdefgh", 4) == "abcd|efgh"

def test_unicode_view_is_printable():
    assert unicode_escape_view("A") == "\\u0041"

def test_marker_validation():
    with pytest.raises(ValueError):
        marker_insert("abc", "x")
