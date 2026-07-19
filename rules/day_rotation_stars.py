import json
from datetime import date, timedelta
from pathlib import Path

from manual_tools.vietnamese_lunar import solar_to_lunar


DEFAULT_RULE_PATH = Path(__file__).parent / "generated" / "day_rotation_stars.json"


def hour_branch(hour):
    return ((int(hour) + 1) // 2) % 12


def day_rotation_template_key(day, month, year, hour):
    birth_date = date(int(year), int(month), int(day))
    if int(hour) == 23:
        birth_date += timedelta(days=1)
    lunar_day, lunar_month, _, lunar_leap = solar_to_lunar(
        birth_date.day, birth_date.month, birth_date.year
    )
    return lunar_day, lunar_month, lunar_leap, hour_branch(hour)


def load_day_rotation_rules(path=DEFAULT_RULE_PATH):
    with Path(path).open("r", encoding="utf-8") as source:
        return json.load(source)


def generate_day_rotation_stars(day, month, year, hour, rules=None):
    rules = rules or load_day_rotation_rules()
    key = ",".join(str(value) for value in day_rotation_template_key(day, month, year, hour))
    template = rules["templates"].get(key)
    if template is None:
        raise KeyError(f"Day-rotation template {key} was not observed in the rule dataset")
    return template