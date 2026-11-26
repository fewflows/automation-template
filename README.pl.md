# fewflows-automation-template

> [English](README.md) · **Polski**

Szablon startowy dla projektów automatyzacji `fewflows` (Python 3.13, `pydantic`, `pytest`, `ruff`, Docker).

## Szybki start

1. **Utwórz i sklonuj projekt:** Na GitHubie kliknij **Use this template → Create a new repository**, a następnie pobierz nowy projekt na dysk do folderu poza OneDrive (np. `C:\projects\`, przez GitHub Desktop lub prosząc agenta o `git clone`).
2. **Dodaj klucz testowy:** W folderze projektu skopiuj `.env.example` jako `.env`, otwórz w edytorze tekstu (np. VS Code) i wklej wyłącznie klucz testowy / sandboxowy z firmowego sejfu (lub od opiekuna technicznego). Hasła zostają lokalnie w `.env` — poza czatem z agentem.
3. **Przygotuj próbkę i buduj kod:** W `tests/fixtures/` zapisz 2–5 fikcyjnych rekordów (bez prawdziwych danych klientów). Logikę automatyzacji rozwijasz z agentem w `src/`.
4. **Sprawdź i wyślij zmiany:** Poproś agenta o uruchomienie testów i wysłanie gotowych zmian jako `Pull Request` do akceptacji.

## Architektura i weryfikacja

- **Kod i tryb bezpieczny (`src/main.py`):** Walidacja wejścia i wyjścia w `pydantic`. Domyślny tryb `--dry-run` zapisuje wynik do `output/sink_preview.json` (granica transportu: `dispatch_live`).
- **Kontener (`Dockerfile`, `.dockerignore`):** Wieloetapowy build na bazie Pythona 3.13 przypiętej przez `@sha256`, zależności zamrożone w `requirements.lock`, `tini` jako `PID 1`, użytkownik `10001:10001`, katalogi `/app` i `/opt/venv` tylko do odczytu (`0:10001`), kompatybilność z `--read-only` + `--cap-drop=ALL`, BuildKit `--mount=type=secret`. Plik `.dockerignore` wpuszcza wyłącznie `pyproject.toml`, `requirements.lock`, `src/**/*.py` oraz `tests/fixtures/**/*.json`.
- **Bramki repozytorium:** Check CI `quality-and-tests` (`ruff`, `pytest`, `--dry-run`, `docker build` + uruchomienie `--read-only`). Zmiany krytyczne nadzoruje `CODEOWNERS`, zasady dla agentów opisuje `AGENTS.md`.

## Uruchamianie lokalne i w kontenerze

```bash
# Środowisko lokalne (Python 3.13, min. >=3.11)
pip install -r requirements.lock
pip install -c requirements.lock -e ".[dev]"
cp .env.example .env

python -m src.main --dry-run
ruff check .
pytest -v
```

```bash
# Docker (build + uruchomienie w trybie --read-only)
docker build -t fewflows-automation:latest .
# Opcjonalnie prywatny indeks pakietów:
# docker build --secret id=pip_conf,src=pip.conf -t fewflows-automation:latest .

docker run --rm \
  --read-only \
  --cap-drop=ALL \
  --security-opt no-new-privileges:true \
  --tmpfs /tmp:rw,noexec,nosuid,size=16m \
  fewflows-automation:latest
```
