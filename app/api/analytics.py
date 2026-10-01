from flask import jsonify
from app.api import api_bp
from app.services.analytics_service import get_analytics

@api_bp.get("/analytics")
def analytics():
    return jsonify(get_analytics())
