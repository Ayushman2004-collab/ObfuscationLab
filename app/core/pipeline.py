import hashlib
import time
from app.core.encoders import apply_encoder
from app.core.transformations import apply_transformation, normalize_pipeline
from app.core.detector import detect, feature_summary

def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()

def run_experiment(sample: str, pipeline):
    steps = normalize_pipeline(pipeline)
    original_detection = detect(sample)
    transformed = sample
    step_metrics = []
    started = time.perf_counter()

    for step in steps:
        step_started = time.perf_counter()
        before_len = len(transformed)
        if step["kind"] == "encoder":
            transformed = apply_encoder(transformed, step["name"], step["params"])
        else:
            transformed = apply_transformation(transformed, step["name"], step["params"])
        step_metrics.append({
            "kind": step["kind"],
            "name": step["name"],
            "input_length": before_len,
            "output_length": len(transformed),
            "duration_ms": round((time.perf_counter() - step_started) * 1000, 3),
        })

    duration_ms = round((time.perf_counter() - started) * 1000, 3)
    transformed_detection = detect(transformed)
    return {
        "transformed_sample": transformed,
        "sample_sha256": sha256_text(sample),
        "transformed_sha256": sha256_text(transformed),
        "input_length": len(sample),
        "output_length": len(transformed),
        "duration_ms": duration_ms,
        "steps": step_metrics,
        "original_detection": original_detection,
        "transformed_detection": transformed_detection,
        "original_features": feature_summary(sample),
        "transformed_features": feature_summary(transformed),
        "detection_changed": original_detection["detected"] != transformed_detection["detected"],
    }
