import argparse
import json
from pathlib import Path

from rules.thien_dieu_brightness_stars import thien_dieu_brightness_template_key


STAR_IDS = {98, 160}


def output_template(item):
    template = [[] for _ in range(12)]
    found = 0
    for palace_index, palace in enumerate(item["output_chart"]["palaces"]):
        for raw_star_id in palace.get("right_stars", ()):
            star_id = int(raw_star_id)
            if star_id in STAR_IDS:
                template[palace_index].append(star_id)
                found += 1
    if found != 1:
        raise ValueError(f"Unexpected Thiên Diêu brightness state count: {found}")
    return template


def run(args):
    templates = {}
    rows = 0
    with args.dataset.open("r", encoding="utf-8") as source:
        for line_number, line in enumerate(source, 1):
            if not line.strip():
                continue
            item = json.loads(line)
            input_data = item["input_data"]
            key = ",".join(
                str(value)
                for value in thien_dieu_brightness_template_key(
                    input_data["day"],
                    input_data["month"],
                    input_data["year"],
                    input_data["hour"],
                    input_data["sex"],
                )
            )
            template = output_template(item)
            previous = templates.setdefault(key, template)
            if previous != template:
                raise ValueError(
                    f"Conflicting Thiên Diêu brightness template at line {line_number}: key {key}"
                )
            rows += 1
            if rows % args.progress_every == 0:
                print(f"Built rules from {rows:,} charts", flush=True)

    artifact = {
        "schema_version": 1,
        "source": str(args.dataset),
        "rows_validated": rows,
        "template_key": [
            "rolled_lunar_year_mod_60",
            "sex",
            "rolled_lunar_day",
            "rolled_lunar_month",
            "lunar_leap",
            "hour_branch",
        ],
        "day_boundary": "23:00 belongs to the next lunar day",
        "screen_slot_order": "extractor palace traversal order",
        "column": "right_stars",
        "star_ids": sorted(STAR_IDS),
        "templates": templates,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(artifact, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"rows_validated": rows, "output": str(args.output)}, indent=2))


def parse_args():
    parser = argparse.ArgumentParser(description="Build Thiên Diêu brightness physical-slot rules.")
    parser.add_argument("dataset", type=Path, nargs="?", default=Path("metadata copy.jsonl"))
    parser.add_argument(
        "--output", type=Path, default=Path("rules/generated/thien_dieu_brightness_stars.json")
    )
    parser.add_argument("--progress-every", type=int, default=100_000)
    return parser.parse_args()


if __name__ == "__main__":
    run(parse_args())