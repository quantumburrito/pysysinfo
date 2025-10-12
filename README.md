# pysysinfo




## Purpose (what it is)

A portable CLI that reports current system state for quick diagnostics and demo-worthy structured output. Emphasis on correctness, portability, and predictable UX.

## What it must do (functional requirements)

### Gather and print:

 - [ ] CPU: logical/physical cores, instantaneous utilization, load average.

- [ ] Memory: total/free/used, percent used.

- [ ] Disks: per-mount usage (total/used/free) and percent used.

- [ ] Top N processes by CPU (and optionally by RSS).

### Output formats:

- [ ] Human (tabular/pretty) and JSON (machine-readable).

- [ ] JSON must be a single object with stable keys (versioned schema in the README).

- [ ] CLI flags (examples; final names in README): --top <N> (default 5), --sort cpu|rss, --json, --pretty, --no-color, --version, --verbose.

- [ ] Exit codes: 0 on success; non-zero on internal error (document error codes).

- [ ] Logging: quiet by default; --verbose emits info to STDERR via Python logging. 
Python documentation

## What it must NOT do (non-goals / exclusions)

- ❌ No long-running daemon, background scheduler, or live-updating TUI.

- ❌ No privileged operations (no sudo, no proc manipulation, no killing processes).

- ❌ No writing outside the working directory (unless user passes an explicit --out path).

- ❌ No network access.

- ❌ No attempt to “forecast” or average across runs—this is a point-in-time snapshot.

## Quality & UX constraints

- [ ] Prints in < 1s on typical laptops/VMs.

- [ ] JSON mode must be stable (keys and types don’t change across runs/versions).

- [ ] Pretty mode: aligned columns; truncation rules documented in README.

- [ ] Works on Linux (primary), macOS; Windows considered stretch.

## Concepts to review (targeted)

How psutil reads CPU/mem/disk/process info; platform portability caveats. 
psutil.readthedocs.io
+1

CLI ergonomics & help UX with Click (flags, defaults, validation). 
click.palletsprojects.com
+1

Python logging levels/handlers vs printing; STDERR vs STDOUT norms. 
Python documentation
+2
docs.python-guide.org
+2

Designing a small output schema (versioning, types, units); documenting contracts.