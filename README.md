# Paypage Ledger

Minimal checkout-page script inventory for small merchants.

Signature: **Mourad.Soltani**

## What it does

PCI DSS 4.x asks merchants to know which scripts run on payment pages and
to notice unexpected changes. Paypage Ledger is a solo-size tool that:

1. Fetches a checkout URL
2. Inventories external `script src` values and SHA-256 hashes of inline scripts
3. Stores a baseline per URL
4. Diffs the next scan and reports added / removed / changed scripts

No browser automation. HTML parse only. Designed to ship in a weekend.

## Run

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8080
```

Health: `GET /health`

Scan (uses local HTML fixture if URL is `fixture://checkout`):

```bash
curl -X POST http://127.0.0.1:8080/scans \
  -H 'content-type: application/json' \
  -d '{"url":"fixture://checkout"}'
```

## Tests

```bash
pytest -q
```

## Stack

- FastAPI + uvicorn
- stdlib HTML parser + hashlib
- pytest

## License

MIT — Mourad.Soltani
