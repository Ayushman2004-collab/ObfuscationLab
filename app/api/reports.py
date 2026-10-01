from flask import Response
from app.api import api_bp
from app.services.report_service import json_report, csv_report

@api_bp.get("/reports/<experiment_id>.json")
def report_json(experiment_id):
    report = json_report(experiment_id)
    if report is None:
        return {"error": "Experiment not found."}, 404
    return Response(report, mimetype="application/json",
                    headers={"Content-Disposition": f'attachment; filename="obfuscationlab-{experiment_id}.json"'})

@api_bp.get("/reports/<experiment_id>.csv")
def report_csv(experiment_id):
    report = csv_report(experiment_id)
    if report is None:
        return {"error": "Experiment not found."}, 404
    return Response(report, mimetype="text/csv",
                    headers={"Content-Disposition": f'attachment; filename="obfuscationlab-{experiment_id}.csv"'})
