import argparse
import json
from collections import Counter
from datetime import date, timedelta
from functools import lru_cache
from pathlib import Path

from .vietnamese_lunar import solar_to_lunar


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


@lru_cache(maxsize=200_000)
def lunar_date(day, month, year):
    return solar_to_lunar(day, month, year)


def projected_feature_keys(sex, day, month, year, hour, minute, yearcalc, monthcalc):
    _, lunar_month, lunar_year, _ = lunar_date(day, month, year)
    if hour == 23:
        rollover_date = date(year, month, day) + timedelta(days=1)
        rat_lunar_day, _, _, _ = lunar_date(
            rollover_date.day, rollover_date.month, rollover_date.year
        )
    else:
        rat_lunar_day = lunar_date(day, month, year)[0]
    lunar_year_stem = lunar_year % 10
    lunar_year_branch = lunar_year % 12
    hour_branch = ((hour + 1) // 2) % 12
    birth_values = (
        lunar_year_stem,
        lunar_year_branch,
        lunar_month,
        rat_lunar_day,
        hour_branch,
        sex,
    )
    view_year_stem = yearcalc % 10
    view_year_branch = yearcalc % 12
    return (
        (birth_values[0],),
        (birth_values[1],),
        (birth_values[2],),
        (birth_values[3],),
        (birth_values[4],),
        (birth_values[5],),
        (birth_values[0], birth_values[2]),
        (birth_values[1], birth_values[2]),
        (birth_values[3], birth_values[2]),
        (birth_values[3], birth_values[4]),
        (birth_values[0], birth_values[4]),
        (birth_values[1], birth_values[4]),
        (birth_values[0], birth_values[2], birth_values[4]),
        (birth_values[1], birth_values[2], birth_values[4]),
        (birth_values[3], birth_values[2], birth_values[4]),
        (birth_values[0], birth_values[2], birth_values[5]),
        (view_year_stem,),
        (view_year_branch,),
        (monthcalc,),
        (view_year_stem, monthcalc),
        (view_year_branch, monthcalc),
        (view_year_stem, view_year_branch, monthcalc),
    )


def input_values(input_data):
    return tuple(int(input_data[name]) for name in (
        "sex", "day", "month", "year", "hour", "minute", "yearcalc", "monthcalc"
    ))


def update_location_map(locations, key, palace_index):
    previous = locations.get(key)
    if previous is None:
        locations[key] = palace_index
        return False
    if previous == palace_index or previous == -1:
        return False
    locations[key] = -1
    return True


def run(args):
    targets = load_targets(args.inventory)
    candidates = BIRTH_CANDIDATES + VIEW_CANDIDATES
    candidate_indexes = {
        star_id: (
            range(len(BIRTH_CANDIDATES))
            if star["category"] == "natal_auxiliary"
            else range(len(BIRTH_CANDIDATES), len(candidates))
        )
        for star_id, star in targets.items()
    }
    location_maps = {
        star_id: [dict() for _ in candidates]
        for star_id in targets
    }
    conflict_counts = {
        star_id: [0 for _ in candidates]
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
            feature_keys = projected_feature_keys(*input_values(item["input_data"]))
            for star_id, palace_index in star_locations(item, targets):
                appearances[star_id] += 1
                for candidate_index in candidate_indexes[star_id]:
                    if update_location_map(
                        location_maps[star_id][candidate_index],
                        feature_keys[candidate_index],
                        palace_index,
                    ):
                        conflict_counts[star_id][candidate_index] += 1
            rows += 1
            if rows % args.progress_every == 0:
                print(f"Analyzed {rows:,} charts", flush=True)

    stars = []
    for star_id, star in targets.items():
        observed = appearances[star_id]
        if not observed:
            continue
        reports = []
        for candidate_index in candidate_indexes[star_id]:
            locations = location_maps[star_id][candidate_index]
            conflicting_keys = conflict_counts[star_id][candidate_index]
            reports.append({
                "features": list(candidates[candidate_index]),
                "keys": len(locations),
                "conflicting_keys": conflicting_keys,
                "is_deterministic": conflicting_keys == 0,
            })
        reports.sort(
            key=lambda result: (
                result["is_deterministic"],
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