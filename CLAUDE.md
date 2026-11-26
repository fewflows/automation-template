# Instrukcja projektu: fewflows automation-template

## Cel repozytorium
Repozytorium stanowi wzorcowy szablon automatyzacji `fewflows` zapewniający deterministyczną walidację danych, bezpieczny tryb poligonowy oraz automatyczną weryfikację jakości w CI.

## Szybki start
1. Przygotuj lokalną konfigurację środowiska: `cp .env.example .env`
2. Uruchom potok w trybie `Test Sink`: `python -m src.main --dry-run`
3. Sprawdź styl i jakość kodu: `ruff check .`
4. Uruchom zestaw testów: `pytest -v`

## Zasady architektury
- Dane wrażliwe, tokeny i klucze API rezydują wyłącznie w lokalnym pliku `.env`, pozostając poza historią Git oraz rozmowami z agentami.
- Zewnętrzne wywołania sieciowe są oddzielone od logiki biznesowej przez granicę transportu i lokalne ujście `Test Sink`.
- Każda zmiana w kodzie przechodzi przez `Pull Request` oraz bramkę weryfikacyjną GitHub Actions CI.
