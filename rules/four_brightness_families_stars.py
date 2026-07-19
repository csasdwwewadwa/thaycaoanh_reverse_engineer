import json
from datetime import date, timedelta
from pathlib import Path

from manual_tools.vietnamese_lunar import solar_to_lunar


DEFAULT_RULE_PATH = Path(__file__).parent / "generated" / "four_brightness_families_stars.json"


def hour_branch(hour):
    return ((int(hour) + 1) // 2) % 12


def four_brightness_families_template_key(day, month, year, hour, sex):
    birth_date = date(int(year), int(month), int(day))
    if int(hour) == 23:
        birth_date += timedelta(days=1)
    lunar_day, lunar_month, lunar_year, lunar_leap = solar_to_lunar(
        birth_date.day, birth_date.month, birth_date.year
    )
    return lunar_year % 60, int(sex), lunar_day, lunar_month, lunar_leap, hour_branch(hour)


def load_four_brightness_families_rules(path=DEFAULT_RULE_PATH):
    with Path(path).open("r", encoding="utf-8") as source:
        return json.load(source)


def generate_four_brightness_families_stars(day, month, year, hour, sex, rules=None):
    rules = rules or load_four_brightness_families_rules()
    key = ",".join(
        str(value) for value in four_brightness_families_template_key(day, month, year, hour, sex)
    )
    template = rules["templates"].get(key)
    if template is None:
        raise KeyError(f"Four brightness families template {key} was not observed in the rule dataset")
    return template