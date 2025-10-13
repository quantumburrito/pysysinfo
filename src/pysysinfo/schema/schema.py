from typing import Any, Dict
import json
schema_version = "1.0"

def make_empty_snapshot(schema_version: str = "1.0") -> str:
    return json.dumps({
        "schema_version": schema_version,
        "timestamp_iso": "",
        "timestamp_unix": 0,
        "platform": {},
        "cpu": {},
        "memory": {},
        "disks": [],
        "processes": [],
        })