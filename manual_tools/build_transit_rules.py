import argparse
import json
from pathlib import Path

from rules.transit_stars import view_year_branch, view_year_stem


RULES = (
    (7, "view_year_branch"),
    (13, "view_year_branch"),
    (42, "view_year_stem"),
    (61, "view_year_stem"),
    (65, "view_year_branch"),
    (75, "view_year_branch"),
    (76, "view_year_branch"),
    (88, "view_year_stem"),
    (128, "view_year_branch"),
)


def transit_output(item, target_ids):
    locations = {}
    template = [[] for _ in range(12)]
    for palace_index, palace in enumerate(item["output_chart"]["palaces"]):
        for column in ("left_stars", "right_stars"):
            for raw_star_id in palace.get(column, ()):
                star_id = int(raw_star_id)
                if star_id in target_ids:
                    if star_id in locations:
                        raise ValueError(f"Transit star {star_id} occurs more than once")
                    locations[star_id] = palace_index
                    template[palace_index].append(star_id)
    return locations, template


def selector_value(selector, yearcalc):
    if selector == "view_year_stem":
        return view_year_stem(yearcalc)
    if selector == "view_year_branch":
        return view_year_branch(yearcalc)
    raise ValueError(f"Unsupported transit selector {selector!r}")


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
            locations, template = transit_output(item, target_ids)
            if set(locations) != target_ids:
                missing = sorted(target_ids - set(locations))
                raise ValueError(f"Missing transit stars at line {line_number}: {missing}")
            yearcalc = item["input_data"]["yearcalc"]
            cycle_key = str(int(yearcalc) % 60)
            previous_template = templates.setdefault(cycle_key, template)
            if previous_template != template:
                raise ValueError(
                    f"Conflicting ordered transit template at line {line_number}: cycle {cycle_key}"
                )
            for star_id, selector in RULES:
                key = str(selector_value(selector, yearcalc))
                location = locations[star_id]
                previous = palace_by_rule[star_id].setdefault(key, location)
                if previous != location:
                    raise ValueError(
                        f"Conflicting transit rule at line {line_number}: "
                        f"star {star_id}, key {key} maps to {previous} and {location}"
                    )
            rows += 1
            if rows % args.progress_every == 0:
                print(f"Built rules from {rows:,} charts", flush=True)

    artifact = {
        "schema_version": 1,
        "source": str(args.dataset),
        "rows_validated": rows,
        "template_key": "yearcalc_mod_60",
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
    parser = argparse.ArgumentParser(description="Build deterministic viewing-year transit star rules.")
    parser.add_argument("dataset", type=Path, nargs="?", default=Path("metadata copy.jsonl"))
    parser.add_argument("--output", type=Path, default=Path("rules/generated/transit_stars.json"))
    parser.add_argument("--progress-every", type=int, default=100_000)
    return parser.parse_args()


if __name__ == "__main__":
    run(parse_args())