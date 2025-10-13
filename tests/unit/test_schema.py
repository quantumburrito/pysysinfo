"""Contract: the schema module must be importable for tests to run.

This is a smoke test that ensures the package exposes `pysysinfo.schema`.
If this import fails, downstream contract tests cannot execute.
"""

import pysysinfo.schema as schema
import json
import time

def test_schema_module_importable():
    # Purpose: Verify the schema module exists and can be imported.
    # Why: Later contract tests depend on this module for constants/functions.
    # Expectation: Import succeeds and module reference is non-None.
    assert schema is not None

def test_schema_top_level_keys_present():
    # Purpose: build a snapshot and assert that the keys exist exactly
    # Why: verify the the top level keys are present in the json output
    # Expectation: top level keys exist as defined in schema.md after snapshot 
    # generation.
    schema_version = schema.schema_version

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
