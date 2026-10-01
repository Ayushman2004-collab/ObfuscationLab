# REST API v1

Base path: `/api/v1`

## Create an experiment
`POST /experiments`

```json
{
  "label": "Marker representation study",
  "sample": "LAB_TEST_MARKER_ALPHA",
  "notes": "Baseline versus Base64",
  "pipeline": [
    {"kind": "encoder", "name": "base64", "params": {}}
  ]
}
```

Allowed encoder names: `base64`, `rot13`, `xor_hex`.
Allowed transform names: `split_join`, `unicode_view`, `marker_view`.
At most 8 steps are accepted. XOR uses a demonstration key supplied in `params.key`; the dashboard uses a fixed lab-only key.

## Other endpoints
- `GET /experiments` — recent experiment metadata.
- `GET /experiments/{id}` — one experiment record.
- `GET /analytics` — aggregate counts.
- `GET /reports/{id}.json` — JSON report download.
- `GET /reports/{id}.csv` — CSV report download.

Health check: `GET /health`.
