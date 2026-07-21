from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .models import Finding


def read_json(path: str | Path) -> Any:
    file_path = Path(path)
    try:
        return json.loads(file_path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise ValueError(f"File not found: {file_path}") from exc
    except json.JSONDecodeError as exc:
        raise ValueError(
            f"Invalid JSON in {file_path}: line {exc.lineno}, column {exc.colno}"
        ) from exc


def load_findings(path: str | Path) -> list[Finding]:
    raw = read_json(path)
    if not isinstance(raw, list):
        raise ValueError("Findings JSON must contain a top-level list.")
    return [Finding.from_dict(item) for item in raw]


def write_text(path: str | Path, content: str) -> None:
    output = Path(path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(content, encoding="utf-8")


def write_json(path: str | Path, content: Any) -> None:
    output = Path(path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        json.dumps(content, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
