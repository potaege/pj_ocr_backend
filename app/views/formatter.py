import json
from pathlib import Path
from typing import Any, Dict, List

_DEFS_DIR = Path(__file__).parent / "defs"
_CACHE: Dict[str, Dict[str, List[str]]] = {}

def _load_table_defs(table: str) -> Dict[str, List[str]]:
    table = table.strip().lower()
    if table in _CACHE:
        return _CACHE[table]

    fp = _DEFS_DIR / f"{table}.json"
    if not fp.exists():
        raise ValueError(f"Unknown table '{table}' (missing defs file: {fp.name})")

    with fp.open("r", encoding="utf-8") as f:
        defs = json.load(f)

    if not isinstance(defs, dict):
        raise ValueError(f"Invalid defs in {fp.name}: must be an object")

    _CACHE[table] = defs
    return defs

def format(data: Dict[str, Any], table: str, view: str) -> Dict[str, Any]:
    defs = _load_table_defs(table)

    view = view.strip().lower()
    if view not in defs:
        raise ValueError(
            f"Unknown view '{view}' for table '{table}'. Allowed: {list(defs.keys())}"
        )

    fields = defs[view]
    if not isinstance(fields, list):
        raise ValueError(f"Invalid view fields for {table}.{view}: must be a list")

    out: Dict[str, Any] = {}

    for key in fields:
        if isinstance(data, dict):
            if key in data:
                out[key] = data[key]
        else:
            if hasattr(data, key):
                out[key] = getattr(data, key)

    return out
