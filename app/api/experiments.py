from flask import current_app, request
from app.api import api_bp
from app.services.experiment_service import create_experiment, list_experiments, get_experiment

@api_bp.post("/experiments")
def create():
    payload = request.get_json(silent=True)
    if not isinstance(payload, dict):
        return {"error": "Expected a JSON object."}, 400
    sample = payload.get("sample")
    if not isinstance(sample, str) or not sample.strip():
        return {"error": "sample must be a non-empty string."}, 400
    if len(sample) > current_app.config["MAX_SAMPLE_LENGTH"]:
        return {"error": "sample exceeds configured character limit."}, 413
    pipeline = payload.get("pipeline", [])
    label = payload.get("label", "Untitled experiment")
    notes = payload.get("notes", "")
    if not isinstance(label, str) or not isinstance(notes, str):
        return {"error": "label and notes must be strings."}, 400
    try:
        result = create_experiment(sample, pipeline, label, notes)
    except (ValueError, TypeError) as exc:
        return {"error": str(exc)}, 400
    # Sample text is returned to the requesting analyst but is not persisted in SQLite.
    return {"experiment": result}, 201

@api_bp.get("/experiments")
def list_all():
    return {"experiments": list_experiments()}

@api_bp.get("/experiments/<experiment_id>")
def detail(experiment_id):
    item = get_experiment(experiment_id)
    if item is None:
        return {"error": "Experiment not found."}, 404
    return {"experiment": item}
