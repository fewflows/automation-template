# syntax=docker/dockerfile:1

# --- Stage 1: Builder ---
FROM python:3.13-slim AS builder

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /build

RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

COPY pyproject.toml ./
COPY src ./src

# BuildKit secret mount: bezpieczne przekazywanie konfiguracji prywatnych indeksów
# (np. --secret id=pip_conf,src=pip.conf) bez utrwalania sekretów w warstwach obrazu.
RUN --mount=type=secret,id=pip_conf,target=/etc/pip.conf,required=false \
    pip install --no-cache-dir .

# --- Stage 2: Hardened Runtime ---
FROM python:3.13-slim AS runtime

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/opt/venv/bin:$PATH"

RUN groupadd --gid 10001 appgroup \
    && useradd --uid 10001 --gid 10001 --shell /usr/sbin/nologin --no-create-home appuser

WORKDIR /app

COPY --from=builder --chown=10001:10001 /opt/venv /opt/venv
COPY --chown=10001:10001 src ./src
COPY --chown=10001:10001 tests/fixtures ./tests/fixtures

USER 10001:10001

ENTRYPOINT ["python", "-m", "src.main"]
CMD ["--dry-run", "--output", "/tmp/sink_preview.json"]
