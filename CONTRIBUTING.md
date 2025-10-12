# CONTRIBUTING.md

# Contributing to `pysysinfo`

Thanks for your interest in improving `pysysinfo`! This document explains how to work on the project, our test-first workflow, and how we manage schema stability and releases.

## Scope & support

* **Platforms:** Linux & macOS for v1.
* **Python:** 3.12+
* **Non-goals:** No daemons, no privileged ops, no network access, no forecasting.

## Architecture at a glance (no code)

* **probe/** — pure data acquisition (cpu, memory, disk, process); no printing, no logging.
* **schema/** — stable, versioned output shape; single source of truth for keys/units.
* **cli/** — I/O and UX (flags, pretty/json rendering, logging, exit codes).
* **config.py / logging.py** — configuration + logging setup for `--verbose`.

## Development setup

1. **Clone & enter repo**

   ```bash
   git clone <your-fork-url>
   cd pysysinfo
   ```
2. **Create a virtual env (any tool is fine)**

   ```bash
   python3.12 -m venv .venv
   source .venv/bin/activate
   ```
3. **Install the package (editable) + test tools**

   ```bash
   pip install -e .
   pip install pytest pytest-cov
   # Optional: ruff, black, mypy, pre-commit
   ```

## Test-first workflow (TDD)

1. **Pick a tiny slice** (one field, one flag, or one error path).
2. **Write one failing test**.
3. **Implement the smallest change** to pass.
4. **Refactor** while keeping tests green.
5. Keep probes **pure** (no I/O). Use CLI only for rendering and logging.

### What to test

* **Unit:** probes (mock/stub `psutil`), renderer alignment/truncation rules.
* **Contract:** snapshot matches **schema v1** (stable keys/units); golden JSONs for Linux/macOS.
* **CLI:** `--json` → data to **STDOUT**; `--verbose` → logs to **STDERR**; exit codes.
* **Perf guard:** one slow test that the full run completes under the 1-second budget.

### Mocks/fixtures

* Prefer `pytest` fixtures + `monkeypatch` to replace `psutil` calls with deterministic data.
* Golden files live under `tests/golden/` and are updated **only** via explicit schema change PRs.

## Branching & PRs

* `main` — always releasable (protected).
* `dev` — integration branch for feature work (protected).
* `feature/*` — short-lived, branch off `dev`, squash-merge into `dev`.

**PR checklist**

* [ ] Tests added/updated and passing locally.
* [ ] No schema drift unless explicitly intended.
* [ ] Docs updated (`README.md`, `SCHEMA.md` as applicable).
* [ ] CI green.

## Commits & changelogs

* Use **clear, descriptive commits**. Conventional Commits (`feat:`, `fix:`, `docs:`…) are welcome but not required.
* We use **SemVer** for the package (`X.Y.Z`) and a **separate** `schema_version` embedded in JSON outputs.

  * Package **PATCH**: bug fixes, no schema/key/type changes.
  * Package **MINOR**: new features, may add fields (schema **MINOR**).
  * Package **MAJOR**: breaking changes; schema **MAJOR** if keys/types/units change.

## Schema changes process (very important)

1. Open a PR with:

   * Proposed change summarized in `SCHEMA.md` (what & why).
   * Bump `schema_version` (e.g., `1.0` → `1.1` for additive, `2.0` for breaking).
   * Update golden JSONs and contract tests.
2. Reviewers verify **backwards compatibility** claims and docs.
3. Merge → release per maintainers’ cadence.

## CLI/UX rules (enforced in tests)

* Data goes to **STDOUT**. Logs/warnings (only under `--verbose`) to **STDERR**.
* Default behavior is documented in `README.md` (pretty vs json). Flags must override defaults predictably.
* Exit code `0` on success; non-zero on internal error. Error codes are documented.

## CI & releases

* CI (GitHub Actions) runs tests on push/PR.
* A tagged commit `vX.Y.Z` triggers the release workflow (see repo’s `.github/workflows/`).
* Maintainers publish to PyPI. Consider TestPyPI first for larger changes.

## Reporting bugs & proposing features

* Open a GitHub issue with:

  * Repro steps, expected vs actual, OS, Python version.
  * For features, state the user story and how it fits within **non-goals**.

## Code of Conduct

* Be kind, specific, and constructive. If we add a formal CoC, it will be linked here.