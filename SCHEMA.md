

# `pysysinfo` JSON Schema — v1.0

**Schema version:** `1.0`
**Status:** Frozen for v1.x of the CLI output.
**Scope:** Linux & macOS, Python 3.12.

## 1) Overview

`pysysinfo --json` emits **one JSON object** with stable keys. Keys, types, and units below are a contract; additive fields require a **schema minor** bump, breaking changes require a **schema major** bump.

* **Units:** sizes in **bytes** (integers); percentages in **0–100** (numbers); durations in **seconds** (numbers).
* **Timestamps:** both ISO-8601 UTC string and UNIX epoch seconds are included.
* **Determinism:** arrays are sorted as specified; ties use documented tie-breakers.
* **Nulls:** only fields marked “nullable” may be `null`. No NaN/Infinity.

## 2) Top-level shape

```json
{
  "schema_version": "1.0",
  "timestamp_iso": "2025-10-12T17:05:23Z",
  "timestamp_unix": 1760288723,
  "platform": { ... },
  "cpu": { ... },
  "memory": { ... },
  "disks": [ ... ],
  "processes": [ ... ]
}
```

### Required keys (all required unless noted)

| Key              | Type    | Description                           |
| ---------------- | ------- | ------------------------------------- |
| `schema_version` | string  | Fixed string for this spec (`"1.0"`). |
| `timestamp_iso`  | string  | ISO-8601 UTC, `YYYY-MM-DDTHH:MM:SSZ`. |
| `timestamp_unix` | integer | UNIX epoch seconds.                   |
| `platform`       | object  | OS metadata (see §3).                 |
| `cpu`            | object  | CPU metrics (see §4).                 |
| `memory`         | object  | Memory metrics (see §5).              |
| `disks`          | array   | Per-mount usage (see §6).             |
| `processes`      | array   | Top-N process snapshot (see §7).      |

---

## 3) `platform` object

| Field     | Type   | Notes                                   |
| --------- | ------ | --------------------------------------- |
| `os`      | string | `linux` or `macos`.                     |
| `release` | string | Kernel/Darwin release string.           |
| `machine` | string | Architecture (e.g., `x86_64`, `arm64`). |

*All fields required; no nulls.*

---

## 4) `cpu` object

| Field                 | Type    | Units / Range | Notes                                                     |
| --------------------- | ------- | ------------- | --------------------------------------------------------- |
| `logical_cores`       | integer | —             | ≥ 1.                                                      |
| `physical_cores`      | integer | —             | ≥ 1; may equal logical on some systems.                   |
| `utilization_percent` | number  | 0–100         | Instantaneous sample. Document sampling window in README. |
| `load_avg_1m`         | number  | —             | Nullable if OS does not provide.                          |
| `load_avg_5m`         | number  | —             | Nullable if OS does not provide.                          |
| `load_avg_15m`        | number  | —             | Nullable if OS does not provide.                          |

*Nullability: only `load_avg_*` may be `null`.*

---

## 5) `memory` object

| Field             | Type    | Units         | Notes                                     |
| ----------------- | ------- | ------------- | ----------------------------------------- |
| `total_bytes`     | integer | bytes         | ≥ 0.                                      |
| `available_bytes` | integer | bytes         | ≥ 0; OS-specific semantics (psutil).      |
| `used_bytes`      | integer | bytes         | ≥ 0.                                      |
| `free_bytes`      | integer | bytes         | ≥ 0.                                      |
| `used_percent`    | number  | percent 0–100 | Derived consistent with psutil semantics. |

*No nulls.*

---

## 6) `disks` array

**Array sorted by** `mountpoint` (ascending, case-sensitive).
**Exclusions:** pseudo-filesystems (e.g., `/proc`, `/sys`, `devfs`, `autofs`); exact lists documented in README.

Each element:

| Field          | Type    | Units | Notes                                                 |
| -------------- | ------- | ----- | ----------------------------------------------------- |
| `mountpoint`   | string  | —     | e.g., `/`, `/home`, `/System/Volumes/Data`.           |
| `filesystem`   | string  | —     | e.g., `ext4`, `apfs`.                                 |
| `device`       | string  | —     | Optional: backing device path; may be empty on macOS. |
| `total_bytes`  | integer | bytes | ≥ 0.                                                  |
| `used_bytes`   | integer | bytes | ≥ 0.                                                  |
| `free_bytes`   | integer | bytes | ≥ 0.                                                  |
| `used_percent` | number  | 0–100 | —                                                     |

*Nullability: none. `device` may be an empty string but not `null`.*

---

## 7) `processes` array

Represents the **top-N processes**, where N is chosen by CLI flag (`--top`, default 5).

**Sorting:**

* Default: by `cpu_percent` **desc**, then `rss_bytes` **desc**, then `pid` **asc** (tie-breaker).
* If CLI `--sort rss`: by `rss_bytes` **desc**, then `cpu_percent` **desc**, then `pid` **asc**.

Each element:

| Field              | Type    | Units / Range | Notes                               |
| ------------------ | ------- | ------------- | ----------------------------------- |
| `pid`              | integer | —             | > 0.                                |
| `name`             | string  | —             | Process name only.                  |
| `cmdline`          | string  | —             | Optional; may be truncated; see §8. |
| `cpu_percent`      | number  | 0–100         | Instantaneous sample.               |
| `rss_bytes`        | integer | bytes         | Resident set size.                  |
| `cpu_time_seconds` | number  | seconds       | Optional; user+system total.        |

*Nullability: optional fields may be omitted or present as strings/numbers; avoid `null` where possible. No NaN/Infinity.*

---

## 8) String limits & truncation

* `processes[].name`: no truncation in JSON.
* `processes[].cmdline`: **may be truncated** in JSON to a documented maximum (e.g., 256 chars). Truncation indicator: ellipsis (`…`) at end.
* Pretty output has its own width rules (documented in README); JSON stays as above.

---

## 9) Streams & exit behavior (summary, detailed in README)

* In `--json` mode, the JSON object is written to **STDOUT**.
* Logs (enabled only with `--verbose`) and errors go to **STDERR**.
* Exit code `0` on success; non-zero on internal error (see README for code table).

---

## 10) Platform notes

* macOS vs Linux differences are limited to:

  * Filesystem types and mount naming.
  * Potential unavailability of some `load_avg_*` fields → they **may be `null`**.

Any additional platform caveats must be added here in a future schema **minor** update.

---

## 11) Minimal example (illustrative)

```json
{
  "schema_version": "1.0",
  "timestamp_iso": "2025-10-12T17:05:23Z",
  "timestamp_unix": 1760288723,
  "platform": {
    "os": "linux",
    "release": "6.8.0-45-generic",
    "machine": "x86_64"
  },
  "cpu": {
    "logical_cores": 8,
    "physical_cores": 4,
    "utilization_percent": 12.5,
    "load_avg_1m": 0.42,
    "load_avg_5m": 0.37,
    "load_avg_15m": 0.35
  },
  "memory": {
    "total_bytes": 16716341248,
    "available_bytes": 10485760000,
    "used_bytes": 6230581248,
    "free_bytes": 420000000,
    "used_percent": 37.3
  },
  "disks": [
    {
      "mountpoint": "/",
      "filesystem": "ext4",
      "device": "/dev/nvme0n1p2",
      "total_bytes": 512110190592,
      "used_bytes": 221000000000,
      "free_bytes": 291110190592,
      "used_percent": 43.1
    }
  ],
  "processes": [
    {
      "pid": 1234,
      "name": "python",
      "cmdline": "python app.py --serve …",
      "cpu_percent": 72.3,
      "rss_bytes": 512000000,
      "cpu_time_seconds": 134.6
    }
  ]
}
```

---

## 12) Changelog

* **1.0 (initial)** — Defines top-level keys; bytes for sizes; 0–100 percents; deterministic sorting for `processes`; optional `cmdline` and `cpu_time_seconds`; `load_avg_*` nullable.
