"""Contract tests for the schema layer

These are contract-level checks:
- the schema module must be importable;
- a snapshot must expose exactly the documented top-level keys;
- generated snapshots must be JSON objects with the correct types/units at the top level.

Notes:
- Compare Python dicts (or JSON-decoted objects), not the serialized strings
  string formating/ordering can cause brittle tests
"""


import json
import time
from datetime import datetime, timezone

import pysysinfo.schema as schema

def test_schema_module_importable():
    # Purpose: Verify the schema module exists and can be imported.
    # Why: Later contract tests depend on this module for constants/functions.
    # Expectation: Import succeeds and module reference is non-None.
    assert schema is not None

def test_schema_top_level_keys_present():
    # Purpose: Assert the snapshot exposes exactly the documented top-level keys.
    # Why: vPrevent silent drift (missing/extra keys) in the public JSON contract.
    # Expectation: Keys match schema.md exactly; values have the expected container types.
    # generation.
    expected_keys = {
        "schema_version",
        "timestamp_iso",
        "timestamp_unix",
        "platform",
        "cpu",
        "memory",
        "disks",
        "processes"
    }

    # If make_empty_snapshot returns a JSON string, decode to a dict first
    raw = schema.make_empty_snapshot(schema.schema_version)
    obj = json.loads(raw) if isinstance(raw, str) else raw

    # Exact key set
    assert set(obj.keys()) == expected_keys

    # Top-level container/type sanity checks (don't validate inner fields here)
    assert isinstance(obj["schema_version"], str)
    assert isinstance(obj["timestamp_iso"], str)
    assert isinstance(obj["timestamp_unix"], int)
    assert isinstance(obj["platform"], dict)
    assert isinstance(obj["cpu"], dict)
    assert isinstance(obj["memory"], dict)
    assert isinstance(obj["disks"], list)
    assert isinstance(obj["processes"], list)


    test_empty_schema = {
        "schema_version": schema_version,
        "timestamp_iso": "",
        "timestamp_unix": 0,
        "platform": {},
        "cpu": {},
        "memory": {},
        "disks": [],
        "processes": [],
    }
    assert schema.make_empty_snapshot(schema.schema_version) == json.dumps(test_empty_schema)


def test_snapshot_creation():
    # Purpose: create a snapshot with specific values
    # Why: verify snapshot creation function
    # Expectation: key value pairs match expectations
    schema_version = schema.schema_version
    test_timestamp_iso = time.time()
    test_timestamp_unix = int(test_timestamp_iso)
    test_platform = {
        "os": "linux",
        "release": "Darwin",
        "machine": "x86_64",
    }
    test_cpu = {
        "logical_cores": 4,
        "physical_cores": 8,
        "utilization_percent": 23.88,
        "load_avg_1m":24.99,
        "load_avg_5m":25.90,
        "load_avg_15m":10.88,
    }
    test_memory = {
        "total_bytes":8000000000,
        "available_bytes":45000000,
        "used_bytes": 890000,
        "free_bytes": 189000,
        "used_percent": 12.00,
    }
    test_disks = [
        {
            "mountpoint":"/",
            "filesystem":"ext4",
            "device":"",
            "total_bytes":124000,
            "used_bytes":12,
            "free_bytes":(124000-12),
            "used_percent":12/124000,
        },
    ]
    test_processes=[
        {
            "pid":123,
            "name":"processes_1",
            "cmdline":"/tty1",
            "cpu_percent":123,
            "rss_bytes":1234,
            "cpu_time_seconds":122.44,
        },
    ]
    test_generated_schema = {
        "schema_version": schema_version,
        "timestamp_iso": test_timestamp_iso,
        "timestamp_unix": test_timestamp_unix,
        "platform": test_platform,
        "cpu": test_cpu,
        "memory": test_memory,
        "disks": test_disks,
        "processes": test_processes,
    }
    generated_snapshot = schema.generate_snapshot(schema_version=schema_version, timestamp_iso = test_timestamp_iso,timestamp_unix=test_timestamp_unix,platform=test_platform,cpu=test_cpu,memory=test_memory,disks=test_disks,processes=test_processes)
    assert generated_snapshot == json.dumps(test_generated_schema)

def test_schema_types():
    pass
