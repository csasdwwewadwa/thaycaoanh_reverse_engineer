import argparse
import json
from pathlib import Path

from rules.major_stars import major_rule_key


def major_template(item):
    return [
        [int(star_id) for star_id in palace.get("major_stars", ())]
        for palace in item["output_chart"]["palaces"]
    ]


def run(args):
    templates = {}
    template_ids = {}
    selectors = {}
    rows = 0
    with args.dataset.open("r", encoding="utf-8") as source:
        for line_number, line in enumerate(source, 1):
            if not line.strip():
                continue
            item = json.loads(line)
            input_data = item["input_data"]
            template = major_template(item)
            template_token = json.dumps(template, separators=(",", ":"))
            template_id = template_ids.setdefault(template_token, len(template_ids))
            templates.setdefault(str(template_id), template)
            key_values = major_rule_key(
                input_data["day"],
                input_data["month"],
                input_data["year"],
                input_data["hour"],
            )
            key = ",".join(str(value) for value in key_values)
            previous = selectors.setdefault(key, template_id)
            if previous != template_id:
                raise ValueError(
                    f"Conflicting major rule at line {line_number}: key {key} maps to {previous} and {template_id}"
                )
            rows += 1
            if rows % args.progress_every == 0:
                print(f"Built rules from {rows:,} charts", flush=True)

    artifact = {
        "schema_version": 1,
        "source": str(args.dataset),
        "rows_validated": rows,
        "key_fields": ["lunar_day", "lunar_month", "lunar_year_stem", "hour_branch"],
        "day_boundary": "23:00 belongs to the next lunar day",
        "template_count": len(templates),
        "selector_count": len(selectors),
        "templates": templates,
        "selectors": selectors,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(artifact, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({
        "rows_validated": rows,
        "template_count": len(templates),
        "selector_count": len(selectors),
        "output": str(args.output),
    }, indent=2))


def parse_args():
    parser = argparse.ArgumentParser(description="Build deterministic major-star rules from scraped charts.")
    parser.add_argument("dataset", type=Path, nargs="?", default=Path("metadata copy.jsonl"))
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("rules/generated/major_stars.json"),
    )
    parser.add_argument("--progress-every", type=int, default=100_000)
    return parser.parse_args()


if __name__ == "__main__":
    run(parse_args())