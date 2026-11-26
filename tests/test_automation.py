"""Testy jednostkowe potoku automatyzacji fewflows."""

import json
from pathlib import Path

import pytest
from pydantic import ValidationError

from src.main import run_pipeline


def test_dry_run_writes_test_sink(tmp_path: Path) -> None:
    """Potwierdza zapis podsumowania do Test Sink oraz poprawne metryki ROAS."""
    input_path = Path("tests/fixtures/sample_campaigns.json")
    output_path = tmp_path / "sink_preview.json"

    result = run_pipeline(input_path=input_path, output_path=output_path, dry_run=True)

    assert result == output_path
    assert output_path.exists()
    payload = json.loads(output_path.read_text(encoding="utf-8"))
    assert payload["total_spend"] == 150.0
    assert payload["total_revenue"] == 475.0
    assert payload["overall_roas"] == 3.17


def test_invalid_negative_spend_raises_validation_error(tmp_path: Path) -> None:
    """Potwierdza odrzucenie rekordu z ujemnym wydatkiem przez walidator Pydantic."""
    invalid_input = tmp_path / "invalid_campaigns.json"
    invalid_input.write_text(
        json.dumps([{"campaign_name": "Invalid Campaign", "spend": -10, "revenue": 100.0}]),
        encoding="utf-8",
    )

    with pytest.raises(ValidationError):
        run_pipeline(
            input_path=invalid_input,
            output_path=tmp_path / "sink_preview.json",
            dry_run=True,
        )


def test_live_mode_requires_api_key(tmp_path: Path) -> None:
    """Potwierdza wymóg obecności klucza API w trybie Live."""
    input_path = Path("tests/fixtures/sample_campaigns.json")

    with pytest.raises(ValueError):
        run_pipeline(
            input_path=input_path,
            output_path=tmp_path / "sink_preview.json",
            dry_run=False,
            api_key=None,
        )
