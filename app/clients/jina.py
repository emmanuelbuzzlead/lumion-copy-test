"""Jina Reader: a company's website as clean text (https://r.jina.ai/<url>).

The consultant research prompt was written around Jina text plus the company description from the
sourcing vendors. Serper is NOT used for this client. Best effort: returns "" when the site cannot be
read, and the caller says so plainly instead of reaching for another vendor.
"""

from __future__ import annotations

import os
import time

import httpx

READER = "https://r.jina.ai/"


def website_text(domain: str, max_chars: int = 6000) -> str:
    key = os.getenv("JINA_API_KEY")
    headers = {"Accept": "text/plain"}
    if key:
        headers["Authorization"] = f"Bearer {key}"
    for attempt in range(2):
        try:
            r = httpx.get(f"{READER}https://{domain}", headers=headers, timeout=40, follow_redirects=True)
        except httpx.HTTPError:
            time.sleep(1.5)
            continue
        if r.status_code == 200 and len(r.text.strip()) > 80:
            return r.text.strip()[:max_chars]
        if r.status_code in (429, 500, 502, 503, 504):
            time.sleep(2 ** attempt)
            continue
        break
    return ""
