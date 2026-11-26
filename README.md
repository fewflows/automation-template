# fewflows-automation-template

> **English** · [Polski](README.pl.md)

Starter template for `fewflows` automation projects (Python 3.13, `pydantic`, `pytest`, `ruff`, Docker).

## Quick start

1. **Create and clone the project:** On GitHub, click **Use this template → Create a new repository**, then clone it to a local folder outside OneDrive (e.g. `C:\projects\`, using GitHub Desktop or asking your agent to run `git clone`).
2. **Add a sandbox key:** Copy `.env.example` to `.env`, open it in a text editor (e.g. VS Code), and paste only a test/sandbox key from the company vault (or technical lead). Credentials stay local in `.env` and out of agent chat.
3. **Prepare sample data and build:** Put 2–5 synthetic records in `tests/fixtures/` (no real customer data). Develop your automation logic with the agent inside `src/`.
4. **Verify and submit:** Ask the agent to run checks and open a `Pull Request` for review.

## Architecture and verification

- **Code and safe execution (`src/main.py`):** Input/output validation with `pydantic`. Default `--dry-run` mode writes output locally to `output/sink_preview.json` (production transport boundary: `dispatch_live`).
- **Container (`Dockerfile`, `.dockerignore`):** Multi-stage build on `@sha256`-pinned Python 3.13, dependencies locked in `requirements.lock`, `tini` as `PID 1`, non-root user `10001:10001`, read-only `/app` and `/opt/venv` (`0:10001`), compatible with `--read-only` + `--cap-drop=ALL`, BuildKit `--mount=type=secret`. `.dockerignore` allows only `pyproject.toml`, `requirements.lock`, `src/**/*.py`, and `tests/fixtures/**/*.json`.
- **Repository gates:** CI check `quality-and-tests` (`ruff`, `pytest`, `--dry-run`, `docker build` + `--read-only` run). Critical files are guarded by `CODEOWNERS`; agent instructions live in `AGENTS.md`.

## Local and container execution

```bash
# Local environment (Python 3.13, min. >=3.11)
pip install -r requirements.lock
pip install -c requirements.lock -e ".[dev]"
cp .env.example .env

python -m src.main --dry-run
ruff check .
pytest -v
```

```bash
# Docker (build + --read-only run)
docker build -t fewflows-automation:latest .
# Optional private package index:
# docker build --secret id=pip_conf,src=pip.conf -t fewflows-automation:latest .

docker run --rm \
  --read-only \
  --cap-drop=ALL \
  --security-opt no-new-privileges:true \
  --tmpfs /tmp:rw,noexec,nosuid,size=16m \
  fewflows-automation:latest
```
