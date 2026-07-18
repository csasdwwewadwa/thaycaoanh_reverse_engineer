import argparse
import itertools
import json
from collections import Counter, defaultdict
from datetime import date, timedelta
from pathlib import Path

try:
    from .vietnamese_lunar import solar_to_lunar
except ImportError:
    from vietnamese_lunar import solar_to_lunar


RAW_FIELDS = ("sex", "day", "month", "year", "hour", "minute", "yearcalc", "monthcalc")
MODULI = (2, 3, 4, 5, 6, 8, 9, 10, 12, 15, 20, 24, 30, 36, 60)


def major_template(item):
    return tuple(
        tuple(int(star_id) for star_id in palace.get("major_stars", ()))
        for palace in item["output_chart"]["palaces"]
    )


def extract_features(input_data):
    raw = {field: int(input_data[field]) for field in RAW_FIELDS}
    birth_date = date(raw["year"], raw["month"], raw["day"])
    lunar_day, lunar_month, lunar_year, lunar_leap = solar_to_lunar(
        raw["day"], raw["month"], raw["year"]
    )
    rat_date = birth_date + timedelta(days=raw["hour"] == 23)
    rat_lunar_day, rat_lunar_month, rat_lunar_year, rat_lunar_leap = solar_to_lunar(
        rat_date.day, rat_date.month, rat_date.year
    )
    features = dict(raw)
    features["birth_ordinal"] = birth_date.toordinal()
    features["birth_year_stem"] = raw["year"] % 10
    features["birth_year_branch"] = raw["year"] % 12
    features["view_year_stem"] = raw["yearcalc"] % 10
    features["view_year_branch"] = raw["yearcalc"] % 12
    features["hour_branch"] = ((raw["hour"] + 1) // 2) % 12
    features["lunar_day"] = lunar_day
    features["lunar_month"] = lunar_month
    features["lunar_year"] = lunar_year
    features["lunar_leap"] = lunar_leap
    features["lunar_year_stem"] = lunar_year % 10
    features["lunar_year_branch"] = lunar_year % 12
    features["rat_lunar_day"] = rat_lunar_day
    features["rat_lunar_month"] = rat_lunar_month
    features["rat_lunar_year_stem"] = rat_lunar_year % 10
    features["rat_lunar_year_branch"] = rat_lunar_year % 12
    features["rat_lunar_leap"] = rat_lunar_leap
    for source in ("year", "yearcalc", "birth_ordinal"):
        for modulus in MODULI:
            features[f"{source}_mod_{modulus}"] = features[source] % modulus
    return features


class DependencyScore:
    def __init__(self, names):
        self.names = names
        self.counts = defaultdict(Counter)

    def add(self, features, label):
        key = tuple(features[name] for name in self.names)
        self.counts[key][label] += 1

    def report(self, total):
        correct = sum(max(labels.values()) for labels in self.counts.values())
        conflicting_keys = sum(1 for labels in self.counts.values() if len(labels) > 1)
        ambiguous_rows = sum(sum(labels.values()) for labels in self.counts.values() if len(labels) > 1)
        return {
            "features": list(self.names),
            "accuracy": correct / total,
            "keys": len(self.counts),
            "conflicting_keys": conflicting_keys,
            "ambiguous_rows": ambiguous_rows,
            "is_deterministic": conflicting_keys == 0,
        }


def candidate_sets(feature_names):
    candidates = [(name,) for name in feature_names]
    compact = (
        "sex",
        "day",
        "month",
        "year",
        "hour",
        "minute",
        "yearcalc",
        "monthcalc",
        "birth_year_stem",
        "birth_year_branch",
        "view_year_stem",
        "view_year_branch",
        "hour_branch",
        "lunar_day",
        "lunar_month",
        "lunar_leap",
        "lunar_year_stem",
        "lunar_year_branch",
    )
    candidates.extend(itertools.combinations(compact, 2))
    candidates.extend((
        ("day", "month", "birth_year_stem", "birth_year_branch", "hour_branch"),
        ("day", "month", "year", "hour_branch"),
        ("birth_ordinal_mod_60", "hour_branch"),
        ("birth_ordinal_mod_60", "birth_year_stem", "hour_branch"),
        ("birth_ordinal_mod_60", "month", "hour_branch"),
        ("lunar_day", "lunar_month"),
        ("lunar_day", "lunar_year_stem"),
        ("lunar_day", "lunar_year_stem", "lunar_year_branch"),
        ("lunar_day", "lunar_month", "lunar_year_stem"),
        ("lunar_day", "lunar_month", "lunar_year_stem", "hour_branch"),
        ("lunar_day", "lunar_month", "lunar_year_stem", "lunar_year_branch", "hour_branch"),
        ("day", "month", "year_mod_60", "hour_branch"),
        tuple(RAW_FIELDS),
    ))
    return list(dict.fromkeys(candidates))


def focused_candidate_sets():
    return (
        ("lunar_day", "lunar_month", "lunar_year_stem"),
        ("lunar_day", "lunar_month", "lunar_year_stem", "hour_branch"),
        ("lunar_day", "lunar_month", "lunar_year_stem", "hour"),
        ("lunar_day", "lunar_month", "lunar_year_stem", "lunar_year_branch", "hour_branch"),
        ("lunar_day", "lunar_month", "lunar_year_stem", "lunar_year_branch", "hour"),
        ("rat_lunar_day", "rat_lunar_month", "rat_lunar_year_stem", "hour_branch"),
        ("rat_lunar_day", "rat_lunar_month", "rat_lunar_year_stem", "rat_lunar_year_branch", "hour_branch"),
        ("lunar_day", "lunar_month", "lunar_year_stem", "sex"),
        ("lunar_day", "lunar_month", "lunar_year_stem", "lunar_leap"),
        ("lunar_day", "lunar_month", "lunar_year_stem", "yearcalc"),
        ("lunar_day", "lunar_month", "lunar_year_stem", "monthcalc"),
        ("lunar_day", "lunar_month", "lunar_year_stem", "minute"),
        ("lunar_day", "lunar_month", "lunar_year_stem", "lunar_year_branch"),
        ("lunar_day", "lunar_month", "lunar_year_stem", "lunar_year_branch", "hour_branch", "sex", "lunar_leap"),
    )


def run(args):
    scores = None
    template_ids = {}
    template_counts = Counter()
    rows = 0
    with args.dataset.open("r", encoding="utf-8") as source:
        for line in source:
            if args.limit and rows >= args.limit:
                break
            if not line.strip():
                continue
            item = json.loads(line)
            template = major_template(item)
            label = template_ids.setdefault(template, len(template_ids))
            features = extract_features(item["input_data"])
            if scores is None:
                candidates = focused_candidate_sets() if args.focused else candidate_sets(tuple(features))
                scores = [DependencyScore(names) for names in candidates]
            for score in scores:
                score.add(features, label)
            template_counts[label] += 1
            rows += 1
            if rows % args.progress_every == 0:
                print(f"Analyzed {rows:,} charts", flush=True)

    results = sorted(
        (score.report(rows) for score in scores or ()),
        key=lambda result: (
            result["is_deterministic"],
            result["accuracy"],
            -len(result["features"]),
            -result["keys"],
        ),
        reverse=True,
    )
    report = {
        "rows": rows,
        "template_count": len(template_ids),
        "template_frequencies": dict(sorted(template_counts.items())),
        "top_dependencies": results[:50],
    }
    args.report.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps(report, indent=2))


def parse_args():
    parser = argparse.ArgumentParser(description="Find deterministic selectors for major-star templates.")
    parser.add_argument("dataset", type=Path, nargs="?", default=Path("metadata copy.jsonl"))
    parser.add_argument("--report", type=Path, default=Path("major_template_analysis.json"))
    parser.add_argument("--limit", type=int, default=0)
    parser.add_argument("--progress-every", type=int, default=25_000)
    parser.add_argument("--focused", action="store_true")
    return parser.parse_args()


if __name__ == "__main__":
    run(parse_args())