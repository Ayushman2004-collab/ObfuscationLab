def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json["mode"] == "synthetic-lab-only"

def test_create_and_retrieve_experiment(client):
    response = client.post("/api/v1/experiments", json={
        "sample": "LAB_TEST_MARKER_ALPHA",
        "label": "API integration",
        "pipeline": [{"kind": "encoder", "name": "base64", "params": {}}]
    })
    assert response.status_code == 201
    experiment_id = response.json["experiment"]["id"]
    detail = client.get(f"/api/v1/experiments/{experiment_id}")
    assert detail.status_code == 200
    assert detail.json["experiment"]["original_detected"] is True

def test_invalid_pipeline_rejected(client):
    response = client.post("/api/v1/experiments", json={
        "sample": "hello",
        "pipeline": [{"kind": "encoder", "name": "execute"}]
    })
    assert response.status_code == 400

def test_empty_sample_rejected(client):
    response = client.post("/api/v1/experiments", json={"sample": " "})
    assert response.status_code == 400

def test_report_downloads(client):
    created = client.post("/api/v1/experiments", json={"sample": "plain text"})
    experiment_id = created.json["experiment"]["id"]
    assert client.get(f"/api/v1/reports/{experiment_id}.json").status_code == 200
    assert client.get(f"/api/v1/reports/{experiment_id}.csv").status_code == 200
