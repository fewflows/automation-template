# syntax=docker/dockerfile:1

# --- Stage 1: Builder ---
# python 3.13.18-slim-trixie
FROM python:3.13-slim@sha256:7249d5587b78209a006dc4a3b5340678f84ea729239193aa559962cd8c1fce50 AS builder

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /build

RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

COPY pyproject.toml requirements.lock ./
COPY src ./src

# BuildKit secret mount: bezpieczne przekazywanie konfiguracji prywatnych indeksów
# (np. --secret id=pip_conf,src=pip.conf) bez utrwalania sekretów w warstwach obrazu.
RUN --mount=type=secret,id=pip_conf,target=/etc/pip.conf,required=false \
    pip install --no-cache-dir -r requirements.lock \
    && pip install --no-cache-dir --no-deps .

# --- Stage 2: Hardened Runtime ---
# python 3.13.18-slim-trixie
FROM python:3.13-slim@sha256:7249d5587b78209a006dc4a3b5340678f84ea729239193aa559962cd8c1fce50 AS runtime

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/opt/venv/bin:$PATH"

RUN apt-get update \
    && apt-get install -y --no-install-recommends tini \
    && rm -rf /var/lib/apt/lists/* \
    && groupadd --gid 10001 appgroup \
    && useradd --uid 10001 --gid 10001 --shell /usr/sbin/nologin --no-create-home appuser

WORKDIR /app

COPY --from=builder --chown=0:10001 /opt/venv /opt/venv
COPY --chown=0:10001 src ./src
COPY --chown=0:10001 tests/fixtures ./tests/fixtures

RUN chmod -R go-w /opt/venv /app

USER 10001:10001

ENTRYPOINT ["/usr/bin/tini", "--", "python", "-m", "src.main"]
CMD ["--dry-run", "--output", "/tmp/sink_preview.json"]
