# fewflows-automation-template

Wzorcowy szablon startowy dla projektów automatyzacji zespołów `fewflows`. Zapewnia ścisłą walidację danych przez Pydantic, lokalny tryb `Test Sink` (`--dry-run`), kontrolę jakości `ruff` oraz automatyczne testy `pytest` w GitHub Actions.

## Utworzenie nowego projektu

1. Wybierz **Use this template** w repozytorium `fewflows/automation-template` na GitHubie i utwórz nowe repozytorium docelowe.
2. Sklonuj nowe repozytorium lokalnie i utwórz środowisko wirtualne Pythona (`>=3.11`).
3. Zainstaluj zależności deweloperskie:
   ```bash
   pip install -e ".[dev]"
   ```
4. Skopiuj konfigurację przykładową do lokalnego pliku środowiskowego:
   ```bash
   cp .env.example .env
   ```

## Uruchamianie i weryfikacja lokalna

- Uruchomienie potoku w trybie bezpiecznym (`Test Sink` zapisuje wynik do `output/sink_preview.json`):
  ```bash
  python -m src.main --dry-run
  ```
- Analiza statyczna kodu i złożoności:
  ```bash
  ruff check .
  ```
- Uruchomienie testów jednostkowych:
  ```bash
  pytest -v
  ```

## Uruchamianie w kontenerze (Docker)

Repozytorium zawiera wieloetapowy `Dockerfile` przygotowany pod izolację wykonania (użytkownik non-root `10001:10001`, system plików tylko do odczytu oraz usunięte uprawnienia jądra Linux).

1. Zbuduj obraz lokalnie (opcjonalnie przekazując konfigurację prywatnego indeksu pakietów przez BuildKit secret mount):
   ```bash
   docker build -t fewflows-automation:latest .
   # Z sekretem BuildKit (bez zapisu sekretu w warstwach obrazu):
   # docker build --secret id=pip_conf,src=pip.conf -t fewflows-automation:latest .
   ```
2. Uruchom kontener w trybie utwardzonym (`--read-only` + `--cap-drop=ALL`):
   ```bash
   docker run --rm \
     --read-only \
     --cap-drop=ALL \
     --security-opt no-new-privileges:true \
     --tmpfs /tmp:rw,noexec,nosuid,size=16m \
     fewflows-automation:latest
   ```

## Praca zespołowa i Pull Request

1. Twórz zmiany na dedykowanej gałęzi roboczej.
2. Upewnij się, że lokalnie przechodzą polecenia `ruff check .`, `pytest -v` oraz `python -m src.main --dry-run`.
3. Wyślij gałąź i otwórz `Pull Request` do gałęzi `main`. Workflow GitHub Actions `CI` uruchamia pełną bramkę jakości automatycznie przed scaleniem.

## Konfiguracja narzędzi agentowych

Repozytorium utrzymuje neutralną konfigurację dla asystentów AI w standardzie multi-agentowym:

- `AGENTS.md` — główna instrukcja projektu dla narzędzi agentowych (w tym Gemini / Antigravity oraz innych środowisk wspierających ten standard).
- `CLAUDE.md` i katalog `.claude/` — opcjonalna konfiguracja kompatybilności dla narzędzi korzystających z tego formatu.
