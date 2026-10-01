from app import create_app

app = create_app()

if __name__ == "__main__":
    # Local-only binding is intentional. Do not expose this lab server publicly.
    app.run(host="127.0.0.1", port=5000, debug=False)
