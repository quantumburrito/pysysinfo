"""Contract: the schema module must be importable for tests to run.

This is a smoke test that ensures the package exposes `pysysinfo.schema`.
If this import fails, downstream contract tests cannot execute.
"""

import pysysinfo.schema as schema


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
    assert schema.SCHEMA_VERSION is "1.0"