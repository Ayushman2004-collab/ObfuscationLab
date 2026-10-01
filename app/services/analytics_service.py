from app.db import get_db

def get_analytics():
    db = get_db()
    total = db.execute("SELECT COUNT(*) FROM experiments").fetchone()[0]
    original = db.execute("SELECT COUNT(*) FROM experiments WHERE original_detected = 1").fetchone()[0]
    transformed = db.execute("SELECT COUNT(*) FROM experiments WHERE transformed_detected = 1").fetchone()[0]
    changed = db.execute(
        "SELECT COUNT(*) FROM experiments WHERE original_detected != transformed_detected"
    ).fetchone()[0]
    rows = db.execute(
        "SELECT created_at, original_detected, transformed_detected FROM experiments ORDER BY created_at DESC LIMIT 20"
    ).fetchall()
    return {
        "total_experiments": total,
        "original_detection_count": original,
        "transformed_detection_count": transformed,
        "detection_state_changed_count": changed,
        "recent": [dict(row) for row in rows],
    }
