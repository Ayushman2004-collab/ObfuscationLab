import pytest
from app.core.pipeline import run_experiment

def test_pipeline_runs_and_hashes():
    result = run_experiment("LAB_TEST_MARKER_ALPHA", [
        {"kind": "encoder", "name": "base64", "params": {}}
    ])
    assert len(result["sample_sha256"]) == 64
    assert result["original_detection"]["detected"] is True
    assert result["transformed_detection"]["detected"] is False

def test_unknown_step_rejected():
    with pytest.raises(ValueError):
        run_experiment("sample", [{"kind": "encoder", "name": "unknown"}])
