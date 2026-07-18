import argparse
import json
from collections import Counter, defaultdict
from pathlib import Path


TRANSIT_PREFIXES = ("L.", "LN.", "ĐV.")


def load_star_names(path):
    with path.open("r", encoding="utf-8") as source:
        records = json.load(source)
    return {int(record["id"]): record["name"] for record in records.values()}


def is_transit_name(name):
    return name is not None and name.startswith(TRANSIT_PREFIXES)


def run(args):
    names = load_star_names(args.star_names)
    major_ids = set()
    source_columns = defaultdict(Counter)
    locations = defaultdict(Counter)
    appearances = Counter()
    rows = 0

    with args.dataset.open("r", encoding="utf-8") as source:
        for line in source:
            if not line.strip():
                continue
            item = json.loads(line)
            palaces = item["output_chart"]["palaces"]
            for palace in palaces:
                major_ids.update(int(star_id) for star_id in palace.get("major_stars", ()))
            for palace_index, palace in enumerate(palaces):
                for column in ("left_stars", "right_stars"):
                    for raw_star_id in palace.get(column, ()):
                        star_id = int(raw_star_id)
                        source_columns[star_id][column] += 1
                        locations[star_id][palace_index] += 1
                        appearances[star_id] += 1
            rows += 1
            if rows % args.progress_every == 0:
                print(f"Profiled {rows:,} charts", flush=True)

    stars = []
    for star_id in sorted(names):
        name = names[star_id]
        if star_id in major_ids:
            category = "major_variant"
        elif is_transit_name(name):
            category = "transit"
        else:
            category = "natal_auxiliary"
        stars.append({
            "id": star_id,
            "name": name,
            "category": category,
            "appearances": appearances[star_id],
            "chart_frequency": appearances[star_id] / rows,
            "source_columns": dict(sorted(source_columns[star_id].items())),
            "possible_palaces": sorted(locations[star_id]),
            "palace_counts": dict(sorted(locations[star_id].items())),
        })

    report = {
        "rows": rows,
        "categories": dict(Counter(star["category"] for star in stars)),
        "stars": stars,
    }
    args.report.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(report["categories"], ensure_ascii=False, indent=2))
    print(f"Wrote {args.report}")


def parse_args():
    parser = argparse.ArgumentParser(description="Profile non-major stars before deterministic rule recovery.")
    parser.add_argument("dataset", type=Path, nargs="?", default=Path("metadata copy.jsonl"))
    parser.add_argument("--star-names", type=Path, default=Path("hash_data.json"))
    parser.add_argument("--report", type=Path, default=Path("non_major_inventory.json"))
    parser.add_argument("--progress-every", type=int, default=100_000)
    return parser.parse_args()


if __name__ == "__main__":
    run(parse_args())