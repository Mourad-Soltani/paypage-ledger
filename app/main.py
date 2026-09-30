# Paypage Ledger — API
# Signature: Mourad.Soltani

from __future__ import annotations

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from app.fixtures import FIXTURES
from app.parser import diff_inventories, inventory_html
from app.store import BaselineStore

APP_NAME = "paypage-ledger"
APP_AUTHOR = "Mourad.Soltani"

store = BaselineStore()
app = FastAPI(title="Paypage Ledger", version="0.1.0")


class ScanRequest(BaseModel):
    url: str = Field(..., min_length=8)
    save_as_baseline: bool = True


@app.get("/health")
def health() -> dict:
    return {
        "ok": True,
        "service": APP_NAME,
        "author": APP_AUTHOR,
    }


@app.post("/scans")
def create_scan(req: ScanRequest) -> dict:
    html = FIXTURES.get(req.url)
    if html is None:
        raise HTTPException(
            status_code=400,
            detail="Only fixture:// URLs are enabled in this MVP (offline health).",
        )
    current = inventory_html(html)
    baseline = store.get(req.url)
    diff = None
    if baseline:
        diff = diff_inventories(baseline, current)
    if req.save_as_baseline or baseline is None:
        store.put(req.url, current)
    return {
        "url": req.url,
        "inventory": current,
        "diff": diff,
        "author": APP_AUTHOR,
    }


@app.delete("/baselines")
def reset_baselines() -> dict:
    store.clear()
    return {"ok": True}
