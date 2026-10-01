import csv
import io
import json
from app.services.experiment_service import get_experiment

def json_report(experiment_id):
    item = get_experiment(experiment_id)
    if item is None:
        return None
    return json.dumps({
        "report_type": "ObfuscationLab experiment report",
        "safety_note": "Synthetic text-only lab results; not a real AV/EDR assessment.",
        "experiment": item,
    }, indent=2)

def csv_report(experiment_id):
    item = get_experiment(experiment_id)
    if item is None:
        return None
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["field", "value"])
    for key in ["id", "created_at", "label", "sample_sha256", "transformed_sha256",
                "input_length", "output_length", "duration_ms",
                "original_detected", "transformed_detected", "notes"]:
        writer.writerow([key, item.get(key)])
    writer.writerow(["pipeline", json.dumps(item["pipeline"])])
    writer.writerow(["original_matches", json.dumps(item["original_matches"])])
    writer.writerow(["transformed_matches", json.dumps(item["transformed_matches"])])
    return output.getvalue()
