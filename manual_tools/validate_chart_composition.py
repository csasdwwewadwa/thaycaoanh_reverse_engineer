import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from chart_generator import generate_chart


SOURCE_PATH = PROJECT_ROOT / "metadata copy.jsonl"
COLUMNS = ("major_stars", "left_stars", "right_stars")


def expected_chart(record):
    return {
        column: [
            [int(star_id) for star_id in palace.get(column, ())]
            for palace in record["output_chart"]["palaces"]
        ]
        for column in COLUMNS
    }


def validate(source_path=SOURCE_PATH):
    matched = 0
    with Path(source_path).open("r", encoding="utf-8") as source:
        for index, line in enumerate(source):
            record = json.loads(line)
            actual = generate_chart(**record["input_data"])
            expected = expected_chart(record)
            if actual != expected:
                for column in COLUMNS:
                    if actual[column] != expected[column]:
                        raise AssertionError(
                            f"Mismatch at record {index} in {column}: "
                            f"input={json.dumps(record['input_data'], ensure_ascii=True)}; "
                            f"actual={actual[column]!r}; expected={expected[column]!r}"
                        )
                raise AssertionError(f"Mismatch at record {index}")
            matched += 1
    print(f"Matched {matched} frozen records exactly.")


if __name__ == "__main__":
    validate()