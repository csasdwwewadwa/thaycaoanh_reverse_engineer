import argparse
import json
from datetime import date, timedelta
from pathlib import Path

from rules.kinh_duong_da_la_stars import kinh_duong_da_la_template_key


FAMILIES = ({72, 134}, {106, 130})


def output_template(item):
    template = [[] for _ in range(12)]
    found = {star_id: 0 for family in FAMILIES for star_id in family}
    for palace_index, palace in enumerate(item["output_chart"]["palaces"]):
        for column in ("left_stars", "right_stars"):
            for raw_star_id in palace.get(column, ()):
                star_id = int(raw_star_id)
                if star_id in found:
                    found[star_id] += 1
                    template[palace_index].append(star_id)

    if any(count > 1 for count in found.values()):
        raise ValueError(f"Duplicate Kinh Duong/Da La star IDs: {found}")
    for family in FAMILIES:
        if sum(found[star_id] for star_id in family) != 1:
            raise ValueError(f"Expected one displayed variant for family {sorted(family)}: {found}")
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
                for value in kinh_duong_da_la_template_key(
                    input_data["day"], input_data["month"], input_data["year"], input_data["hour"]
                )
            )
            template = output_template(item)
            previous = templates.setdefault(key, template)
            if previous != template:
                raise ValueError(
                    f"Conflicting Kinh Duong/Da La template at line {line_number}: key {key}"
                )
            rows += 1
            if rows % args.progress_every == 0:
                print(f"Built rules from {rows:,} charts", flush=True)

    artifact = {
        "schema_version": 1,
        "source": str(args.dataset),
        "rows_validated": rows,
        "template_key": ["rolled_lunar_year_stem", "rolled_lunar_month", "lunar_leap", "hour_branch"],
        "day_boundary": "23:00 belongs to the next lunar day",
        "screen_slot_order": "extractor palace traversal order",
        "families": [[72, 134], [106, 130]],
        "templates": templates,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(artifact, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"rows_validated": rows, "output": str(args.output)}, indent=2))


def parse_args():
    parser = argparse.ArgumentParser(description="Build physical-slot rules for Kinh Duong and Da La.")
    parser.add_argument("dataset", type=Path, nargs="?", default=Path("metadata copy.jsonl"))
    parser.add_argument("--output", type=Path, default=Path("rules/generated/kinh_duong_da_la_stars.json"))
    parser.add_argument("--progress-every", type=int, default=100_000)
    return parser.parse_args()


if __name__ == "__main__":
    run(parse_args())