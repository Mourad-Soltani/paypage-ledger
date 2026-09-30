# Paypage Ledger — health and scan tests
# Signature: Mourad.Soltani

from fastapi.testclient import TestClient

from app.main import app, store
from app.parser import inventory_html, diff_inventories
from app.fixtures import CHECKOUT_HTML_V1, CHECKOUT_HTML_V2


client = TestClient(app)


def setup_function() -> None:
    store.clear()


def test_health_ok() -> None:
    r = client.get("/health")
    assert r.status_code == 200
    body = r.json()
    assert body["ok"] is True
    assert body["author"] == "Mourad.Soltani"
    assert body["service"] == "paypage-ledger"


def test_inventory_extracts_scripts() -> None:
    inv = inventory_html(CHECKOUT_HTML_V1)
    assert "https://js.stripe.com/v3/" in inv["external_scripts"]
    assert inv["inline_count"] == 1
    assert inv["external_count"] == 2


def test_diff_detects_change() -> None:
    a = inventory_html(CHECKOUT_HTML_V1)
    b = inventory_html(CHECKOUT_HTML_V2)
    d = diff_inventories(a, b)
    assert d["changed"] is True
    assert "https://cdn.unknown.example/inject.js" in d["added_external"]
    assert "https://pay.example.com/checkout.js" in d["removed_external"]


def test_scan_fixture_and_second_scan_no_diff() -> None:
    r1 = client.post("/scans", json={"url": "fixture://checkout"})
    assert r1.status_code == 200
    r2 = client.post("/scans", json={"url": "fixture://checkout"})
    assert r2.status_code == 200
    assert r2.json()["diff"]["changed"] is False


def test_rejects_live_url_in_mvp() -> None:
    r = client.post("/scans", json={"url": "https://example.com/pay"})
    assert r.status_code == 400
