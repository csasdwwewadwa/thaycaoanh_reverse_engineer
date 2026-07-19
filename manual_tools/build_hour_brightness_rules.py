import argparse
import json
from pathlib import Path

from rules.hour_brightness_stars import hour_branch


TARGET_IDS = {10, 11, 192, 193}
FAMILIES = ({10, 192}, {11, 193})


def output_template(item):
    template = [[] for _ in range(12)]
    found = {star_id: 0 for star_id in TARGET_IDS}
    for palace_index, palace in enumerate(item["output_chart"]["palaces"]):
        for column in ("left_stars", "right_stars"):
            for raw_star_id in palace.get(column, ()):
                star_id = int(raw_star_id)
                if star_id in TARGET_IDS:
                    found[star_id] += 1
                    template[palace_index].append(star_id)
    if any(count > 1 for count in found.values()):
        raise ValueError(f"Duplicate hour-brightness star IDs: {found}")
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
            key = str(hour_branch(item["input_data"]["hour"]))
            template = output_template(item)
            previous = templates.setdefault(key, template)
            if previous != template:
                raise ValueError(
                    f"Conflicting hour-brightness template at line {line_number}: hour branch {key}"
                )
            rows += 1
            if rows % args.progress_every == 0:
                print(f"Built rules from {rows:,} charts", flush=True)

    artifact = {
        "schema_version": 1,
        "source": str(args.dataset),
        "rows_validated": rows,
        "template_key": "hour_branch",
        "families": [[10, 192], [11, 193]],
        "templates": templates,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(artifact, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"rows_validated": rows, "output": str(args.output)}, indent=2))


def parse_args():
    parser = argparse.ArgumentParser(description="Build hour-driven brightness-state star rules.")
    parser.add_argument("dataset", type=Path, nargs="?", default=Path("metadata copy.jsonl"))
    parser.add_argument("--output", type=Path, default=Path("rules/generated/hour_brightness_stars.json"))
    parser.add_argument("--progress-every", type=int, default=100_000)
    return parser.parse_args()


if __name__ == "__main__":
    run(parse_args())