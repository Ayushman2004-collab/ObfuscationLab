import os
from flask import Flask, render_template
from app.db import init_db
from app.logging_config import configure_logging
from app.api import api_bp

def create_app(test_config=None):
    app = Flask(__name__, template_folder="../web/templates", static_folder="../web/static")
    app.config.from_mapping(
        SECRET_KEY=os.getenv("SECRET_KEY", "local-development-only-change-me"),
        DATABASE=os.getenv("DATABASE_PATH", "instance/obfuscationlab.sqlite3"),
        MAX_CONTENT_LENGTH=int(os.getenv("MAX_CONTENT_LENGTH", "65536")),
        MAX_SAMPLE_LENGTH=int(os.getenv("MAX_SAMPLE_LENGTH", "10000")),
        JSON_SORT_KEYS=False,
    )
    if test_config:
        app.config.update(test_config)

    os.makedirs(os.path.dirname(app.config["DATABASE"]) or ".", exist_ok=True)
    configure_logging(app)
    init_db(app)
    app.register_blueprint(api_bp, url_prefix="/api/v1")

    @app.get("/")
    def dashboard():
        return render_template("dashboard.html")

    @app.get("/health")
    def health():
        return {"status": "ok", "service": "ObfuscationLab", "mode": "synthetic-lab-only"}

    @app.errorhandler(413)
    def too_large(_error):
        return {"error": "Request too large", "detail": "Reduce the request body size."}, 413

    @app.errorhandler(404)
    def not_found(_error):
        if _error.__class__.__name__ == "NotFound" and getattr(_error, "description", ""):
            return {"error": "Not found"}, 404
        return {"error": "Not found"}, 404

    return app
