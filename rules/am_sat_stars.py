import json
from datetime import date, timedelta
from pathlib import Path

from manual_tools.vietnamese_lunar import solar_to_lunar


DEFAULT_RULE_PATH = Path(__file__).parent / "generated" / "am_sat_stars.json"


def am_sat_template_key(day, month, year, hour):
    birth_date = date(int(year), int(month), int(day))
    if int(hour) == 23:
        birth_date += timedelta(days=1)
    _, lunar_month, _, _ = solar_to_lunar(birth_date.day, birth_date.month, birth_date.year)
    return lunar_month


def load_am_sat_rules(path=DEFAULT_RULE_PATH):
    with Path(path).open("r", encoding="utf-8") as source:
        return json.load(source)


def generate_am_sat_stars(day, month, year, hour, rules=None):
    rules = rules or load_am_sat_rules()
    key = str(am_sat_template_key(day, month, year, hour))
    template = rules["templates"].get(key)
    if template is None:
        raise KeyError(f"Am Sat template for rolled lunar month {key} was not observed")
    return template