# pysysinfo

## Purpose

A portable CLI that reports current system state for quick diagnostics and demo-worthy structured output. Emphasis on correctness, portability, and predictable UX.

## Platforms & requirements

* **Supported (v1):** Linux (primary), macOS
* **Python:** 3.12+
* **Out of scope (v1):** Windows

## What it does (functional requirements)

### Gather and print (point-in-time snapshot)

* [ ] **CPU:** logical/physical cores, instantaneous utilization, load average
* [ ] **Memory:** total/free/used, percent used
* [ ] **Disks:** per-mount usage (total/used/free) and percent used
* [ ] **Processes:** top N by CPU (optionally by RSS)

### Output formats & flags

* [ ] **Human (pretty)** and **JSON** (machine-readable)
* [ ] JSON is a **single object** with **stable keys** (see **Schema** below)
* [ ] Flags (tentative): `--top <N>` (default 5), `--sort cpu|rss`, `--json`, `--pretty`, `--no-color`, `--version`, `--verbose`
* [ ] **Exit codes:** `0` on success; non-zero for internal errors (documented below)
* [ ] **Logging:** quiet by default; `--verbose` emits info to **STDERR** via Python logging

### Streams (contract)

* **STDOUT:** data (pretty table or JSON)
* **STDERR:** logs/warnings (only with `--verbose`) and error messages

## What it does **not** do (non-goals)

* ❌ No long-running daemon, background scheduler, or live-updating TUI
* ❌ No privileged operations (no sudo, no proc manipulation, no killing processes)
* ❌ No writing outside the working directory (unless user passes an explicit `--out` path)
* ❌ No network access
* ❌ No forecasting or cross-run averaging (it’s a **snapshot**)

## Quality & UX constraints

* [ ] Prints in **< 1 s** on typical laptops/VMs
* [ ] JSON mode is **stable** (keys/types don’t change across runs/versions)
* [ ] Pretty mode: aligned columns; **truncation rules** documented
* [ ] Deterministic ordering (sections, mounts, processes) for diff-friendly output

## Schema

* A **versioned schema** governs the JSON object shape (keys, types, and units).
* The JSON includes `"schema_version": "1.0"` in v1.
* See **SCHEMA.md** for the current schema and change log.

## Exit codes (initial draft)

* `0` — success
* `10` — probe failure / internal error (fatal)
* `11` — CLI argument/validation error
* (Finalize after first implementation pass; keep this list short and documented.)

## Defaults (initial draft)

* Default output when attached to a TTY: **pretty**
* Default output when piped: **JSON**
* Flags always override defaults. Final behavior will be documented and tested.

## Performance note

* The CLI aims to complete under 1 second. If it exceeds the budget, a **notice is logged to STDERR only when `--verbose` is set** (non-fatal).

## Install (placeholder)

* PyPI install instructions will be added after the first release.

## Development

* See **CONTRIBUTING.md** for TDD workflow, testing, schema rules, and release process.

## References & further reading

* **psutil (CPU/mem/disk/process):** [https://psutil.readthedocs.io](https://psutil.readthedocs.io)
* **Click (CLI ergonomics):** [https://click.palletsprojects.com](https://click.palletsprojects.com)
* **Python logging:** [https://docs.python.org/3/library/logging.html](https://docs.python.org/3/library/logging.html)
* **Schema design basics:** [https://json-schema.org/learn](https://json-schema.org/learn)

