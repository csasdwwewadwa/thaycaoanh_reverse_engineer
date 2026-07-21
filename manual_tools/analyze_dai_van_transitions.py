"""Report observed Dai Van transformation rows for repeated natal charts."""

from __future__ import annotations

import argparse
import json
from collections import defaultdict
from datetime import date, timedelta
from pathlib import Path

from manual_tools.vietnamese_lunar import solar_to_lunar
from rules.luu_nien_transformation_stars import (
    ANNUAL_TRANSFORMATIONS,
    NATAL_STAR_IDS,
    _slot_for_star,
)
from rules.major_stars import generate_major_stars
from rules.natal_auxiliary_stars import generate_natal_auxiliary_stars
from rules.van_xuong_van_khuc_stars import generate_van_xuong_van_khuc_stars
from rules.year_branch_rotation_stars import generate_year_branch_rotation_stars


DAI_VAN_IDS = {9, 30, 90, 97}
NATURAL_YEAR_BRANCH_OFFSET = 4


def _natal_templates(data):
    return (
        generate_major_stars(data["day"], data["month"], data["year"], data["hour"]),
        generate_natal_auxiliary_stars(
            data["sex"], data["day"], data["month"], data["year"], data["hour"]
        ),
        generate_van_xuong_van_khuc_stars(
            data["day"], data["month"], data["year"], data["hour"]
        ),
        generate_year_branch_rotation_stars(
            data["day"], data["month"], data["year"], data["hour"]
        ),
    )


def observed_dai_van_rows(data, output_chart):
    positions = {}
    for slot, palace in enumerate(output_chart["palaces"]):
        for column in ("left_stars", "right_stars"):
            for star_id in palace.get(column, ()):
                star_id = int(star_id)
                if star_id in DAI_VAN_IDS:
                    positions[star_id] = slot

    target = tuple(positions[star_id] for star_id in (30, 97, 9, 90))
    templates = _natal_templates(data)
    return [
        row
        for row, names in enumerate(ANNUAL_TRANSFORMATIONS)
        if tuple(
            _slot_for_star(templates, NATAL_STAR_IDS[name], name) for name in names
        )
        == target
    ]


def natal_state(data):
    birth_date = date(
        int(data["year"]), int(data["month"]), int(data["day"])
    ) + timedelta(days=int(data["hour"]) == 23)
    _, lunar_month, lunar_year, _ = solar_to_lunar(
        birth_date.day, birth_date.month, birth_date.year
    )
    year_stem = (lunar_year - NATURAL_YEAR_BRANCH_OFFSET) % 10
    hour_branch = ((int(data["hour"]) + 1) // 2) % 12
    men_branch = (lunar_month - hour_branch) % 12
    men_stem = (2 * (year_stem % 5) + men_branch) % 10
    return {
        "lunar_year": lunar_year,
        "lunar_month": lunar_month,
        "men_stem": men_stem,
        "men_branch": men_branch,
        "year_stem": year_stem,
    }


def run(source_path, minimum_observations):
    grouped = defaultdict(list)
    with Path(source_path).open("r", encoding="utf-8") as source:
        for index, line in enumerate(source):
            item = json.loads(line)
            data = item["input_data"]
            key = tuple(data[name] for name in ("sex", "day", "month", "year", "hour"))
            grouped[key].append((index, data, item["output_chart"]))

    reported = 0
    for records in grouped.values():
        view_years = {int(data["yearcalc"]) for _, data, _ in records}
        if len(view_years) < minimum_observations:
            continue

        records.sort(key=lambda record: int(record[1]["yearcalc"]))
        first_data = records[0][1]
        state = natal_state(first_data)
        transitions = [
            {
                "source_line": index,
                "view_year": int(data["yearcalc"]),
                "view_month": int(data["monthcalc"]),
                "lunar_age": int(data["yearcalc"]) - state["lunar_year"] + 1,
                "rows": observed_dai_van_rows(data, output_chart),
            }
            for index, data, output_chart in records
        ]
        print(json.dumps({"natal_state": state, "transitions": transitions}, ensure_ascii=True))
        reported += 1

    print(f"Reported {reported} natal charts with {minimum_observations}+ view years.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("source", nargs="?", default="metadata copy.jsonl")
    parser.add_argument("--minimum-observations", type=int, default=3)
    args = parser.parse_args()
    run(args.source, args.minimum_observations)