import json
from datetime import date, timedelta
from pathlib import Path

from manual_tools.vietnamese_lunar import solar_to_lunar


DEFAULT_RULE_PATH = Path(__file__).parent / "generated" / "major_stars.json"


def hour_branch(hour):
    return ((int(hour) + 1) // 2) % 12


def major_rule_key(day, month, year, hour):
    birth_date = date(int(year), int(month), int(day))
    if int(hour) == 23:
        birth_date += timedelta(days=1)
    lunar_day, lunar_month, lunar_year, _ = solar_to_lunar(
        birth_date.day, birth_date.month, birth_date.year
    )
    return lunar_day, lunar_month, lunar_year % 10, hour_branch(hour)


def load_major_rules(path=DEFAULT_RULE_PATH):
    with Path(path).open("r", encoding="utf-8") as source:
        return json.load(source)


def generate_major_stars(day, month, year, hour, rules=None):
    rules = rules or load_major_rules()
    key = ",".join(str(value) for value in major_rule_key(day, month, year, hour))
    template_id = rules["selectors"].get(key)
    if template_id is None:
        raise KeyError(f"Major-star rule key {key} was not observed in the rule dataset")
    return rules["templates"][str(template_id)]