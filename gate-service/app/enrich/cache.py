from __future__ import annotations

import json
from datetime import datetime
from datetime import timedelta
from pathlib import Path

CACHE_DIR = Path("data/cache")
CACHE_DIR.mkdir(parents=True, exist_ok=True)

KEV_CACHE = CACHE_DIR / "kev.json"

CACHE_TTL = timedelta(hours=24)


def cache_exists() -> bool:
    return KEV_CACHE.exists()


def cache_expired() -> bool:
    if not cache_exists():
        return True

    modified = datetime.fromtimestamp(
        KEV_CACHE.stat().st_mtime
    )

    return datetime.now() - modified > CACHE_TTL


def load_cache() -> dict:

    with KEV_CACHE.open(
        "r",
        encoding="utf-8",
    ) as f:
        return json.load(f)


def save_cache(data: dict) -> None:

    with KEV_CACHE.open(
        "w",
        encoding="utf-8",
    ) as f:
        json.dump(
            data,
            f,
            indent=2,
        )