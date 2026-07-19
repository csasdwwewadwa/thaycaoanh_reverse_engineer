import json
from datetime import date, timedelta
from pathlib import Path

from manual_tools.vietnamese_lunar import solar_to_lunar


DEFAULT_RULE_PATH = Path(__file__).parent / "generated" / "natal_auxiliary_stars.json"


def hour_branch(hour):
    return ((int(hour) + 1) // 2) % 12


def rolled_lunar_day(day, month, year, hour):
    birth_date = date(int(year), int(month), int(day))
    if int(hour) == 23:
        birth_date += timedelta(days=1)
    lunar_day, _, _, _ = solar_to_lunar(birth_date.day, birth_date.month, birth_date.year)
    return lunar_day


def natal_auxiliary_template_key(sex, day, month, year, hour):
    return int(sex), rolled_lunar_day(day, month, year, hour), hour_branch(hour)


def load_natal_auxiliary_rules(path=DEFAULT_RULE_PATH):
    with Path(path).open("r", encoding="utf-8") as source:
        return json.load(source)


def generate_natal_auxiliary_stars(sex, day, month, year, hour, rules=None):
    rules = rules or load_natal_auxiliary_rules()
    key = ",".join(str(value) for value in natal_auxiliary_template_key(sex, day, month, year, hour))
    template = rules["templates"].get(key)
    if template is None:
        raise KeyError(f"Natal auxiliary template {key} was not observed in the rule dataset")
    return template