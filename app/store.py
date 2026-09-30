# Paypage Ledger — in-memory baseline store
# Signature: Mourad.Soltani

from __future__ import annotations

from typing import Dict


class BaselineStore:
    def __init__(self) -> None:
        self._data: Dict[str, dict] = {}

    def get(self, url: str) -> dict | None:
        return self._data.get(url)

    def put(self, url: str, inventory: dict) -> None:
        self._data[url] = inventory

    def clear(self) -> None:
        self._data.clear()
