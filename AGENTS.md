# AGENTS.md — Instrukcja projektu fewflows/automation-template

Uniwersalny plik kontekstu i zasad pracy dla narzędzi agentowych (Gemini / Antigravity oraz innych asystentów zgodnych ze standardem `AGENTS.md`).

## Cel repozytorium

Repozytorium stanowi szablon startowy dla projektów automatyzacji `fewflows`. Zapewnia ścisłą walidację danych wejściowych i wyjściowych przez `pydantic`, lokalny tryb poligonowy `Test Sink` (`--dry-run`), kontrolę jakości `ruff` oraz automatyczną bramkę testową `pytest` w GitHub Actions (`quality-and-tests`).

## Komendy weryfikacyjne

```bash
pip install -e ".[dev]"
cp .env.example .env
python -m src.main --dry-run
ruff check .
pytest -v
```

## Zasady architektury i kodu

- **Python i typowanie:** Kod źródłowy powstaje w Pythonie `>=3.11` z jawnymi adnotacjami typów oraz modelami `pydantic` na granicach wejścia i wyjścia danych.
- **Granica transportu i tryb bezpieczny:** Domyślnym trybem uruchomienia jest `--dry-run`, który kieruje wynik do lokalnego `Test Sink` (`output/sink_preview.json`). Wywołania zewnętrzne są odseparowane za granicą transportu (`dispatch_live`).
- **Deterministyczne testy:** Testy jednostkowe w `tests/` opierają się na zamrożonych próbkach danych w `tests/fixtures/` bez wykonywania połączeń sieciowych.
- **Izolacja sekretów:** Klucze API, tokeny i konfiguracja środowiska rezydują wyłącznie w lokalnym pliku `.env` (poza historią Git i kontekstem promptów). Szablon zmiennych znajduje się w `.env.example`.

## Przepływ pracy i Git

- Gałąź `main` jest chroniona regułami repozytorium. Wszystkie zmiany trafiają do niej wyłącznie przez gałąź roboczą i `Pull Request`.
- Przed wysłaniem zmian na zdalne repozytorium wymagane jest lokalne przejście `ruff check .`, `pytest -v` oraz `python -m src.main --dry-run`.
- Scalenie `Pull Request` wymaga zielonego statusu sprawdzenia `quality-and-tests`.
- Komunikaty commitów stosują konwencję Conventional Commits (`feat:`, `fix:`, `docs:`, `chore:`, `ci:`).
