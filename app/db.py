import sqlite3
from flask import current_app, g

SCHEMA = '''
CREATE TABLE IF NOT EXISTS experiments (
    id TEXT PRIMARY KEY,
    created_at TEXT NOT NULL,
    label TEXT NOT NULL,
    sample_sha256 TEXT NOT NULL,
    transformed_sha256 TEXT NOT NULL,
    input_length INTEGER NOT NULL,
    output_length INTEGER NOT NULL,
    pipeline_json TEXT NOT NULL,
    duration_ms REAL NOT NULL,
    original_detected INTEGER NOT NULL,
    transformed_detected INTEGER NOT NULL,
    original_matches_json TEXT NOT NULL,
    transformed_matches_json TEXT NOT NULL,
    notes TEXT NOT NULL DEFAULT ''
);
CREATE INDEX IF NOT EXISTS idx_experiments_created ON experiments(created_at DESC);
'''

def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(current_app.config["DATABASE"])
        g.db.row_factory = sqlite3.Row
        g.db.execute("PRAGMA foreign_keys = ON")
    return g.db

def close_db(_error=None):
    db = g.pop("db", None)
    if db is not None:
        db.close()

def init_db(app):
    with app.app_context():
        db = sqlite3.connect(app.config["DATABASE"])
        db.executescript(SCHEMA)
        db.commit()
        db.close()
    app.teardown_appcontext(close_db)
