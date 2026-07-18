import argparse
import json
from collections import Counter, defaultdict
from pathlib import Path

from .analyze_major_templates import DependencyScore, extract_features


BIRTH_CANDIDATES = (
    ("lunar_year_stem",),
    ("lunar_year_branch",),
    ("lunar_month",),
    ("rat_lunar_day",),
    ("hour_branch",),
    ("sex",),
    ("lunar_year_stem", "lunar_month"),
    ("lunar_year_branch", "lunar_month"),
    ("rat_lunar_day", "lunar_month"),
    ("rat_lunar_day", "hour_branch"),
    ("lunar_year_stem", "hour_branch"),
    ("lunar_year_branch", "hour_branch"),
    ("lunar_year_stem", "lunar_month", "hour_branch"),
    ("lunar_year_branch", "lunar_month", "hour_branch"),
    ("rat_lunar_day", "lunar_month", "hour_branch"),
    ("lunar_year_stem", "lunar_month", "sex"),
)

VIEW_CANDIDATES = (
    ("view_year_stem",),
    ("view_year_branch",),
    ("monthcalc",),
    ("view_year_stem", "monthcalc"),
    ("view_year_branch", "monthcalc"),
    ("view_year_stem", "view_year_branch", "monthcalc"),
)


def load_targets(path):
    report = json.loads(path.read_text(encoding="utf-8"))
    return {
        int(star["id"]): star
        for star in report["stars"]
        if star["category"] != "major_variant" and star["appearances"]
    }


def star_locations(item, target_ids):
    for palace_index, palace in enumerate(item["output_chart"]["palaces"]):
        for column in ("left_stars", "right_stars"):
            for raw_star_id in palace.get(column, ()):
                star_id = int(raw_star_id)
                if star_id in target_ids:
                    yield star_id, palace_index


def run(args):
    targets = load_targets(args.inventory)
    candidates = BIRTH_CANDIDATES + VIEW_CANDIDATES
    scores = {
        star_id: [DependencyScore(candidate) for candidate in candidates]
        for star_id in targets
    }
    appearances = Counter()
    rows = 0

    with args.dataset.open("r", encoding="utf-8") as source:
        for line in source:
            if args.limit and rows >= args.limit:
                break
            if not line.strip():
                continue
            item = json.loads(line)
            features = extract_features(item["input_data"])
            for star_id, palace_index in star_locations(item, targets):
                appearances[star_id] += 1
                for score in scores[star_id]:
                    score.add(features, palace_index)
            rows += 1
            if rows % args.progress_every == 0:
                print(f"Analyzed {rows:,} charts", flush=True)

    stars = []
    for star_id, star in targets.items():
        observed = appearances[star_id]
        if not observed:
            continue
        reports = [score.report(observed) for score in scores[star_id]]
        reports.sort(
            key=lambda result: (
                result["is_deterministic"],
                result["accuracy"],
                -len(result["features"]),
                -result["keys"],
            ),
            reverse=True,
        )
        stars.append({
            "id": star_id,
            "name": star["name"],
            "category": star["category"],
            "observations": observed,
            "top_dependencies": reports[:8],
        })

    report = {"rows": rows, "stars": stars}
    args.report.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    deterministic = sum(
        star["top_dependencies"][0]["is_deterministic"] for star in stars
    )
    print(f"Wrote {args.report}; {deterministic}/{len(stars)} stars have a deterministic candidate.")


def parse_args():
    parser = argparse.ArgumentParser(description="Score compact selectors for non-major star locations.")
    parser.add_argument("dataset", type=Path, nargs="?", default=Path("metadata copy.jsonl"))
    parser.add_argument("--inventory", type=Path, default=Path("non_major_inventory.json"))
    parser.add_argument("--report", type=Path, default=Path("non_major_dependency_analysis.json"))
    parser.add_argument("--limit", type=int, default=0)
    parser.add_argument("--progress-every", type=int, default=25_000)
    return parser.parse_args()


if __name__ == "__main__":
    run(parse_args())