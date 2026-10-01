import logging
import os
from logging.handlers import RotatingFileHandler

def configure_logging(app):
    os.makedirs("logs", exist_ok=True)
    handler = RotatingFileHandler("logs/obfuscationlab.log", maxBytes=1_000_000, backupCount=3)
    handler.setFormatter(logging.Formatter(
        "%(asctime)s %(levelname)s %(name)s %(message)s"
    ))
    handler.setLevel(logging.INFO)
    if not app.logger.handlers:
        app.logger.addHandler(handler)
    app.logger.setLevel(logging.INFO)
