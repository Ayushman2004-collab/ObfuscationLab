from app.core.detector import detect, feature_summary

def test_synthetic_marker_match():
    assert detect("LAB_TEST_MARKER_ALPHA")["detected"] is True

def test_unmarked_text_does_not_match():
    assert detect("ordinary training text")["detected"] is False

def test_feature_summary():
    assert feature_summary("abc")["length"] == 3
