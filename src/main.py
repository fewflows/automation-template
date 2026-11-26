"""Główny moduł potoku automatyzacji fewflows."""

import argparse
import json
import os
from pathlib import Path
from typing import Any

from pydantic import BaseModel, Field


class CampaignRecord(BaseModel):
    """Walidowany rekord kampanii marketingowej."""

    campaign_name: str
    spend: float = Field(ge=0.0)
    revenue: float = Field(ge=0.0)


def compute_roas(spend: float, revenue: float) -> float:
    """Oblicza wskaźnik ROAS zaokrąglony do dwóch miejsc po przecinku."""
    if spend == 0.0:
        return 0.0
    return round(revenue / spend, 2)


def compute_summary(records: list[CampaignRecord]) -> dict[str, Any]:
    """Wylicza łączne wydatki, przychód, ROAS oraz zestawienie kampanii."""
    total_spend = round(sum(record.spend for record in records), 2)
    total_revenue = round(sum(record.revenue for record in records), 2)
    campaigns = [
        {
            "campaign_name": record.campaign_name,
            "spend": record.spend,
            "revenue": record.revenue,
            "roas": compute_roas(record.spend, record.revenue),
        }
        for record in records
    ]
    return {
        "total_spend": total_spend,
        "total_revenue": total_revenue,
        "overall_roas": compute_roas(total_spend, total_revenue),
        "campaigns": campaigns,
    }


def load_records(input_path: Path) -> list[CampaignRecord]:
    """Wczytuje i waliduje listę kampanii z pliku JSON."""
    raw_items = json.loads(input_path.read_text(encoding="utf-8"))
    return [CampaignRecord.model_validate(item) for item in raw_items]


def dispatch_live(payload: dict[str, Any], api_key: str) -> None:
    """Granica transportu produkcyjnego dla danych wyjściowych potoku."""
    _ = (payload, api_key)
    raise NotImplementedError("Podłącz docelowy transport produkcyjny po przejściu na Staging")


def run_pipeline(
    input_path: Path,
    output_path: Path,
    dry_run: bool = True,
    api_key: str | None = None,
) -> Path:
    """Uruchamia potok walidacji i agregacji w trybie Test Sink lub Live."""
    records = load_records(input_path)
    payload = compute_summary(records)

    if dry_run:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(
            json.dumps(payload, indent=2, ensure_ascii=False),
            encoding="utf-8",
        )
        return output_path

    if not api_key:
        raise ValueError("Tryb Live wymaga skonfigurowanej zmiennej API_KEY")

    dispatch_live(payload, api_key)
    return output_path


def build_parser() -> argparse.ArgumentParser:
    """Buduje parser argumentów wiersza poleceń."""
    parser = argparse.ArgumentParser(description="Szablon potoku automatyzacji fewflows")
    parser.add_argument(
        "--input",
        type=Path,
        default=Path("tests/fixtures/sample_campaigns.json"),
        help="Ścieżka do wejściowego pliku JSON z kampaniami.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("output/sink_preview.json"),
        help="Ścieżka docelowa dla lokalnego Test Sink.",
    )
    mode_group = parser.add_mutually_exclusive_group()
    mode_group.add_argument(
        "--dry-run",
        action="store_const",
        const=True,
        dest="dry_run",
        help="Uruchamia potok z zapisem do lokalnego Test Sink (tryb domyślny).",
    )
    mode_group.add_argument(
        "--live",
        action="store_const",
        const=False,
        dest="dry_run",
        help="Uruchamia potok przez granicę transportu produkcyjnego.",
    )
    parser.set_defaults(dry_run=True)
    return parser


def main() -> None:
    """Punkt wejścia CLI."""
    args = build_parser().parse_args()
    api_key = os.environ.get("API_KEY")
    result_path = run_pipeline(
        input_path=args.input,
        output_path=args.output,
        dry_run=args.dry_run,
        api_key=api_key,
    )
    print(f"Pipeline completed. Output target: {result_path.as_posix()}")


if __name__ == "__main__":
    main()
