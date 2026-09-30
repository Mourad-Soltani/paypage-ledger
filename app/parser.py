# Paypage Ledger — HTML script inventory
# Signature: Mourad.Soltani

from __future__ import annotations

import hashlib
from html.parser import HTMLParser
from typing import List


class ScriptInventoryParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.external: List[str] = []
        self.inline_chunks: List[str] = []
        self._in_script = False
        self._buffer: List[str] = []
        self._current_src: str | None = None

    def handle_starttag(self, tag: str, attrs) -> None:
        if tag.lower() != "script":
            return
        attr_map = {k.lower(): v for k, v in attrs}
        src = attr_map.get("src")
        self._in_script = True
        self._buffer = []
        self._current_src = src.strip() if src else None
        if self._current_src:
            self.external.append(self._current_src)

    def handle_data(self, data: str) -> None:
        if self._in_script and not self._current_src:
            self._buffer.append(data)

    def handle_endtag(self, tag: str) -> None:
        if tag.lower() != "script" or not self._in_script:
            return
        if not self._current_src:
            body = "".join(self._buffer).strip()
            if body:
                self.inline_chunks.append(body)
        self._in_script = False
        self._buffer = []
        self._current_src = None


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def inventory_html(html: str) -> dict:
    parser = ScriptInventoryParser()
    parser.feed(html)
    parser.close()
    inline_hashes = [sha256_text(chunk) for chunk in parser.inline_chunks]
    return {
        "external_scripts": sorted(set(parser.external)),
        "inline_hashes": sorted(set(inline_hashes)),
        "external_count": len(set(parser.external)),
        "inline_count": len(set(inline_hashes)),
    }


def diff_inventories(baseline: dict, current: dict) -> dict:
    b_ext = set(baseline.get("external_scripts", []))
    c_ext = set(current.get("external_scripts", []))
    b_in = set(baseline.get("inline_hashes", []))
    c_in = set(current.get("inline_hashes", []))
    return {
        "added_external": sorted(c_ext - b_ext),
        "removed_external": sorted(b_ext - c_ext),
        "added_inline": sorted(c_in - b_in),
        "removed_inline": sorted(b_in - c_in),
        "changed": bool((c_ext ^ b_ext) or (c_in ^ b_in)),
    }
