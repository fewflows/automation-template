---
paths:
  - "src/**"
  - "tests/**"
---

# Reguły kodu i testowania w Pythonie

- Waliduj wszystkie dane wejściowe i wyjściowe przy użyciu modeli `pydantic`.
- Uruchamiaj potok domyślnie w jawnym trybie `--dry-run`, kierując wynik do lokalnego `Test Sink` (`output/sink_preview.json`).
- Opieraj testy na zamrożonych próbkach danych w katalogu `tests/fixtures/`.
- Przechowuj klucze API i konfigurację środowiska wyłącznie w zmiennych środowiskowych ładowanych z lokalnego pliku `.env`.
- Weryfikuj każdą zmianę poprzez pełne przejście `ruff check .` oraz `pytest -v`.
