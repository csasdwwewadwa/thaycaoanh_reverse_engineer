import argparse
import json
from pathlib import Path

from rules.natal_auxiliary_stars import (
    hour_branch,
    natal_auxiliary_template_key,
    rolled_lunar_day,
)


RULES = (
    (37, "hour_branch"),
    (50, "sex"),
    (69, "rolled_lunar_day_hour_branch"),
    (87, "sex"),
    (112, "hour_branch"),
    (119, "rolled_lunar_day_hour_branch"),
)


def auxiliary_output(item, target_ids):
    locations = {}
    template = [[] for _ in range(12)]
    for palace_index, palace in enumerate(item["output_chart"]["palaces"]):
        for column in ("left_stars", "right_stars"):
            for raw_star_id in palace.get(column, ()):
                star_id = int(raw_star_id)
                if star_id in target_ids:
                    if star_id in locations:
                        raise ValueError(f"Natal auxiliary star {star_id} occurs more than once")
                    locations[star_id] = palace_index
                    template[palace_index].append(star_id)
    return locations, template


def selector_value(selector, input_data):
    if selector == "sex":
        return int(input_data["sex"])
    if selector == "hour_branch":
        return hour_branch(input_data["hour"])
    if selector == "rolled_lunar_day_hour_branch":
        return (
            rolled_lunar_day(
                input_data["day"], input_data["month"], input_data["year"], input_data["hour"]
            ),
            hour_branch(input_data["hour"]),
        )
    raise ValueError(f"Unsupported natal auxiliary selector {selector!r}")


def run(args):
    target_ids = {star_id for star_id, _ in RULES}
    palace_by_rule = {star_id: {} for star_id in target_ids}
    templates = {}
    rows = 0
    with args.dataset.open("r", encoding="utf-8") as source:
        for line_number, line in enumerate(source, 1):
            if not line.strip():
                continue
            item = json.loads(line)
            input_data = item["input_data"]
            locations, template = auxiliary_output(item, target_ids)
            if set(locations) != target_ids:
                missing = sorted(target_ids - set(locations))
                raise ValueError(f"Missing natal auxiliary stars at line {line_number}: {missing}")
            template_key = ",".join(
                str(value)
                for value in natal_auxiliary_template_key(
                    input_data["sex"], input_data["day"], input_data["month"], input_data["year"], input_data["hour"]
                )
            )
            previous_template = templates.setdefault(template_key, template)
            if previous_template != template:
                raise ValueError(
                    f"Conflicting ordered natal auxiliary template at line {line_number}: key {template_key}"
                )
            for star_id, selector in RULES:
                key = ",".join(str(value) for value in (selector_value(selector, input_data),))
                location = locations[star_id]
                previous = palace_by_rule[star_id].setdefault(key, location)
                if previous != location:
                    raise ValueError(
                        f"Conflicting natal auxiliary rule at line {line_number}: "
                        f"star {star_id}, key {key} maps to {previous} and {location}"
                    )
            rows += 1
            if rows % args.progress_every == 0:
                print(f"Built rules from {rows:,} charts", flush=True)

    artifact = {
        "schema_version": 1,
        "source": str(args.dataset),
        "rows_validated": rows,
        "template_key": ["sex", "rolled_lunar_day", "hour_branch"],
        "day_boundary": "23:00 belongs to the next lunar day",
        "templates": templates,
        "rules": [
            {
                "id": star_id,
                "selector": selector,
                "palace_by_key": palace_by_rule[star_id],
            }
            for star_id, selector in RULES
        ],
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(artifact, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"rows_validated": rows, "output": str(args.output)}, indent=2))


def parse_args():
    parser = argparse.ArgumentParser(description="Build deterministic natal auxiliary star rules.")
    parser.add_argument("dataset", type=Path, nargs="?", default=Path("metadata copy.jsonl"))
    parser.add_argument("--output", type=Path, default=Path("rules/generated/natal_auxiliary_stars.json"))
    parser.add_argument("--progress-every", type=int, default=100_000)
    return parser.parse_args()


if __name__ == "__main__":
    run(parse_args())