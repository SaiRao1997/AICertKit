from __future__ import annotations
import hashlib
from pathlib import Path
from typing import Iterable

def read_text_safe(path: Path, limit_bytes: int = 1_000_000) -> str:
    try:
        with open(path, "rb") as f:
            data = f.read(limit_bytes)
        return data.decode("utf-8", errors="ignore")
    except Exception:
        return ""

def file_sha256(path: Path) -> str:
    h = hashlib.sha256()
    try:
        with open(path, "rb") as f:
            for chunk in iter(lambda: f.read(65536), b""):
                h.update(chunk)
    except Exception:
        pass
    return h.hexdigest()

def walk_files(root: Path, include_hidden: bool = False) -> Iterable[Path]:
    for p in root.rglob("*"):
        if p.is_file():
            parts = p.relative_to(root).parts
            if not include_hidden and any(part.startswith(".") for part in parts):
                continue
            yield p
