import json
from datetime import date, timedelta
from pathlib import Path

from manual_tools.vietnamese_lunar import solar_to_lunar


DEFAULT_RULE_PATH = Path(__file__).parent / "generated" / "thien_khoi_thien_viet_stars.json"


def thien_khoi_thien_viet_template_key(day, month, year, hour):
    birth_date = date(int(year), int(month), int(day))
    if int(hour) == 23:
        birth_date += timedelta(days=1)
    _, _, lunar_year, _ = solar_to_lunar(birth_date.day, birth_date.month, birth_date.year)
    return lunar_year % 10


def load_thien_khoi_thien_viet_rules(path=DEFAULT_RULE_PATH):
    with Path(path).open("r", encoding="utf-8") as source:
        return json.load(source)


def generate_thien_khoi_thien_viet_stars(day, month, year, hour, rules=None):
    rules = rules or load_thien_khoi_thien_viet_rules()
    key = str(thien_khoi_thien_viet_template_key(day, month, year, hour))
    template = rules["templates"].get(key)
    if template is None:
        raise KeyError(f"Thien Khoi/Thien Viet template {key} was not observed in the rule dataset")
    return template