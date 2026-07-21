import argparse
import json
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from rules.luu_nien_transformation_stars import generate_luu_nien_transformation_stars


STAR_IDS = {8, 53, 83, 122}
COLUMNS = ("left_stars", "right_stars")


def expected_template(item):
    template = {column: [[] for _ in range(12)] for column in COLUMNS}
    for slot, palace in enumerate(item["output_chart"]["palaces"]):
        for column in COLUMNS:
            template[column][slot] = [
                int(star_id) for star_id in palace.get(column, ()) if int(star_id) in STAR_IDS
            ]
    return template


def validate(dataset, progress_every):
    matched = 0
    with Path(dataset).open("r", encoding="utf-8") as source:
        for line_number, line in enumerate(source, 1):
            if not line.strip():
                continue
            item = json.loads(line)
            input_data = item["input_data"]
            actual = generate_luu_nien_transformation_stars(
                input_data["day"],
                input_data["month"],
                input_data["year"],
                input_data["hour"],
                input_data["sex"],
                input_data["yearcalc"],
            )
            expected = expected_template(item)
            if actual != expected:
                raise AssertionError(
                    f"Mismatch at line {line_number}: "
                    f"input={json.dumps(input_data, ensure_ascii=True)}; "
                    f"actual={actual!r}; expected={expected!r}"
                )
            matched += 1
            if matched % progress_every == 0:
                print(f"Matched {matched:,} Luu Nien records", flush=True)
    print(f"Matched {matched:,} Luu Nien records exactly.")


def parse_args():
    parser = argparse.ArgumentParser(description="Validate the deterministic Luu Nien transformation rule.")
    parser.add_argument("dataset", type=Path, nargs="?", default=PROJECT_ROOT / "metadata copy.jsonl")
    parser.add_argument("--progress-every", type=int, default=100_000)
    return parser.parse_args()


if __name__ == "__main__":
    arguments = parse_args()
    validate(arguments.dataset, arguments.progress_every)