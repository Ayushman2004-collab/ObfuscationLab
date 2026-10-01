# ObfuscationLab v2
### Security Transformation & Detection Analysis Platform

ObfuscationLab is a controlled, text-only research platform for examining how harmless content transformations affect deterministic **synthetic** static-matching rules. It is structured as a small security engineering service: a Flask application factory, versioned REST API, ordered experiment pipeline, SQLite persistence, analytics dashboard, downloadable reports, structured logging, tests and Docker support.

> **Safety boundary:** This is not a malware builder, payload generator, antivirus bypass tool or EDR testing product. It does not execute submitted text or interact with real security products. Use harmless training strings only.

## Engineering capabilities

- Ordered, allowlisted transformation pipelines.
- Base64, ROT13 and XOR-to-hex text representations.
- Split/join, Unicode escape and marker-insertion display transformations.
- Fixed synthetic lab rules (`LAB_TEST_MARKER_ALPHA/BETA/GAMMA`).
- Baseline-versus-transformed detection comparison.
- SHA-256 integrity identifiers, character metrics and per-step timing.
- SQLite experiment history; raw sample text is not persisted.
- REST API, analytics dashboard, JSON/CSV exports.
- Request validation, size limits, parameterized database access and rotating logs.
- Unit and integration test suites; Docker packaging.

## Architecture

See [docs/architecture.md](docs/architecture.md), [docs/methodology.md](docs/methodology.md), [docs/threat-model.md](docs/threat-model.md) and [docs/api.md](docs/api.md).

## Quick start — VS Code on Windows

1. Install Python 3.10+ and Visual Studio Code.
2. Open the `ObfuscationLab_v2` folder in VS Code.
3. Open **Terminal → New Terminal**.
4. Create a virtual environment:

   ```powershell
   py -m venv .venv
   .venv\Scripts\Activate.ps1
   ```

   If PowerShell blocks activation, run `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass`, then activate again. Alternatively use Command Prompt: `.venv\Scripts\activate.bat`.

5. Install dependencies:

   ```powershell
   python -m pip install --upgrade pip
   pip install -r requirements.txt
   ```

6. Start the application:

   ```powershell
   python run.py
   ```

7. Open `http://127.0.0.1:5000` in your browser.

The app creates the SQLite database under `instance/` and a rotating log under `logs/` on first run.

## Run tests

```powershell
pytest -v
```

Coverage report:

```powershell
pytest --cov=app --cov-report=term-missing
```

## Docker

With Docker Desktop running:

```powershell
docker compose up --build
```

Open `http://127.0.0.1:5000`. The compose configuration binds to localhost and mounts the database, reports and logs directories.

## API example

```powershell
$body = @{
  label = "Base64 marker study"
  sample = "LAB_TEST_MARKER_ALPHA"
  pipeline = @(
    @{ kind = "encoder"; name = "base64"; params = @{} }
  )
} | ConvertTo-Json -Depth 6

Invoke-RestMethod -Uri "http://127.0.0.1:5000/api/v1/experiments" `
  -Method Post -ContentType "application/json" -Body $body
```

See [docs/api.md](docs/api.md) for endpoint details.

## Repository layout

```text
ObfuscationLab_v2/
├── app/
│   ├── api/                 # Versioned REST endpoints
│   ├── core/                # Pure transformation and detection logic
│   ├── services/            # Experiment, analytics and report services
│   ├── db.py                # SQLite schema and connection lifecycle
│   └── logging_config.py
├── web/
│   ├── templates/           # Jinja dashboard
│   └── static/              # CSS and JavaScript
├── tests/
│   ├── unit/
│   └── integration/
├── docs/
├── instance/                # Local SQLite database (generated)
├── logs/                    # Application logs (generated)
├── reports/
├── Dockerfile
├── docker-compose.yml
└── run.py
```

## Security and privacy notes

- Keep the service bound to localhost. It is not designed for public deployment.
- Do not submit confidential, personal, proprietary or executable content.
- The database stores experiment metadata, hashes and detector outcomes, not raw sample text.
- JSON/CSV reports contain experiment metadata and hashes, not raw sample content.
- Transformations produce text representations only; no result is executed or loaded as a program.
- The dashboard loads Chart.js and fonts from public CDNs; an offline deployment can vendor these assets locally.

## Suggested internship demonstration

1. Explain the problem: static signatures are deterministic pattern checks and representations can change what a simple rule observes.
2. Show the architecture and the separation between API, core engine, services and persistence.
3. Run a baseline synthetic marker experiment with no transformations.
4. Run the same marker through a Base64 representation and compare the synthetic match state.
5. Inspect hashes, timing, history, analytics and exported report.
6. Explain the limits: this is a controlled synthetic experiment, not evidence about production AV/EDR efficacy.

## Future engineering extensions

- Role-based analyst accounts and audit trails.
- Configurable defensive rule packs with versioning.
- Background job processing for large offline datasets.
- Database migrations and CI pipeline.
- Offline-bundled frontend assets and signed report exports.

## License
For educational and defensive research use. Add an organization-approved license before public redistribution.
