from pathlib import Path
import csv
import json

import pandas as pd


def load_sample_data(path: str | None = None) -> list[dict[str, str]]:
    default_path = Path(__file__).resolve().parents[2] / "data" / "csv" / "sample_customers.csv"
    target_path = Path(path) if path else default_path

    with target_path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def load_sample_dataset(data_dir: str | None = None) -> list[dict[str, object]]:
    base_dir = Path(data_dir) if data_dir else Path(__file__).resolve().parents[2] / "data"
    datasets: list[dict[str, object]] = []

    for data_file in sorted(base_dir.glob("*.parquet")):
        control_candidates = [
            data_file.parent / f"{data_file.name}.ctrl.csv",
            data_file.with_suffix(".ctrl.csv"),
            data_file.parent / "csv" / f"{data_file.stem}.ctrl.csv",
            data_file.parent / f"{data_file.stem}.ctrl.csv",
        ]

        control_file = next((candidate for candidate in control_candidates if candidate.exists()), None)
        if control_file is None:
            control_file = data_file.parent / f"{data_file.name}.ctrl.csv"

        business_date = ""
        record_count = 0
        rows: list[dict[str, str]] = []

        frame = pd.read_parquet(data_file)
        rows = frame.to_dict(orient="records")
        record_count = len(rows)

        if control_file.exists():
            with control_file.open(newline="", encoding="utf-8") as handle:
                control_rows = list(csv.DictReader(handle))
                if control_rows:
                    business_date = control_rows[0].get("business_date", "")

        datasets.append(
            {
                "data_file": data_file,
                "control_file": control_file,
                "business_date": business_date,
                "record_count": record_count,
                "rows": rows,
            }
        )

    return datasets


if __name__ == "__main__":
    datasets = load_sample_dataset()
    for dataset in datasets:
        print(
            json.dumps(
                {
                    "data_file": dataset["data_file"].name,
                    "control_file": dataset["control_file"].name,
                    "business_date": dataset["business_date"],
                    "record_count": dataset["record_count"],
                },
                indent=2,
            )
        )
