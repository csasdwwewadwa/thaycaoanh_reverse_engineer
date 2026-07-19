import json
from collections import Counter
from datetime import date, timedelta

from manual_tools.vietnamese_lunar import solar_to_lunar

STAR_IDS = {8, 53, 83, 122}
templates = {}
rows = 0

with open("metadata copy.jsonl", encoding="utf-8") as source:
    for line_number, line in enumerate(source, 1):
        item = json.loads(line)
        data = item["input_data"]

        birth_date = date(
            int(data["year"]),
            int(data["month"]),
            int(data["day"]),
        )
        if int(data["hour"]) == 23:
            birth_date += timedelta(days=1)

        lunar_day, lunar_month, lunar_year, lunar_leap = solar_to_lunar(
            birth_date.day,
            birth_date.month,
            birth_date.year,
        )

        key = (
            int(data["yearcalc"]) % 60,
            lunar_year % 60,
            int(data["sex"]),
            lunar_day,
            lunar_month,
            lunar_leap,
            ((int(data["hour"]) + 1) // 2) % 12,
        )

        template = {
            "left_stars": [[] for _ in range(12)],
            "right_stars": [[] for _ in range(12)],
        }
        counts = Counter()

        for palace_index, palace in enumerate(item["output_chart"]["palaces"]):
            for column_name in template:
                for raw_star_id in palace.get(column_name, ()):
                    star_id = int(raw_star_id)
                    if star_id in STAR_IDS:
                        template[column_name][palace_index].append(star_id)
                        counts[star_id] += 1

        if set(counts) != STAR_IDS or any(count != 1 for count in counts.values()):
            raise AssertionError(
                f"Unexpected IDs at record {line_number}: {dict(counts)}"
            )

        previous = templates.setdefault(key, template)
        if previous != template:
            raise AssertionError(
                f"Collision at record {line_number}, key = {key}\n"
                f"Previous: {previous}\n"
                f"Current:  {template}"
            )

        rows += 1

print(
    f"PASS: {STAR_IDS} are deterministic across {rows:,} charts "
    f"with {len(templates):,} templates."
)