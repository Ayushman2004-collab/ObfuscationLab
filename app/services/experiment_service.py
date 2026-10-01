import json
import uuid
from datetime import datetime, timezone
from app.db import get_db
from app.core.pipeline import run_experiment

def create_experiment(sample, pipeline, label="Untitled experiment", notes=""):
    result = run_experiment(sample, pipeline)
    experiment_id = str(uuid.uuid4())
    created_at = datetime.now(timezone.utc).isoformat(timespec="seconds")
    db = get_db()
    db.execute(
        '''INSERT INTO experiments (
            id, created_at, label, sample_sha256, transformed_sha256,
            input_length, output_length, pipeline_json, duration_ms,
            original_detected, transformed_detected, original_matches_json,
            transformed_matches_json, notes
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
        (
            experiment_id, created_at, label[:100], result["sample_sha256"],
            result["transformed_sha256"], result["input_length"], result["output_length"],
            json.dumps(pipeline), result["duration_ms"],
            int(result["original_detection"]["detected"]),
            int(result["transformed_detection"]["detected"]),
            json.dumps(result["original_detection"]["matches"]),
            json.dumps(result["transformed_detection"]["matches"]), notes[:500],
        )
    )
    db.commit()
    return {"id": experiment_id, "created_at": created_at, "label": label, **result}

def list_experiments(limit=100):
    rows = get_db().execute(
        "SELECT * FROM experiments ORDER BY created_at DESC LIMIT ?", (limit,)
    ).fetchall()
    return [serialize_row(row) for row in rows]

def get_experiment(experiment_id):
    row = get_db().execute("SELECT * FROM experiments WHERE id = ?", (experiment_id,)).fetchone()
    return serialize_row(row) if row else None

def serialize_row(row):
    if row is None:
        return None
    item = dict(row)
    item["pipeline"] = json.loads(item.pop("pipeline_json"))
    item["original_matches"] = json.loads(item.pop("original_matches_json"))
    item["transformed_matches"] = json.loads(item.pop("transformed_matches_json"))
    item["original_detected"] = bool(item["original_detected"])
    item["transformed_detected"] = bool(item["transformed_detected"])
    return item
