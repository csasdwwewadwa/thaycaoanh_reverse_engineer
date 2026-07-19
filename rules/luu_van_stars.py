import json
from datetime import date, timedelta
from pathlib import Path

from manual_tools.vietnamese_lunar import solar_to_lunar


DEFAULT_RULE_PATH = Path(__file__).parent / "generated" / "luu_van_stars.json"


def luu_van_template_key(day, month, year, hour, yearcalc):
    birth_date = date(int(year), int(month), int(day))
    if int(hour) == 23:
        birth_date += timedelta(days=1)
    _, _, lunar_year, _ = solar_to_lunar(birth_date.day, birth_date.month, birth_date.year)
    return int(yearcalc) % 60, lunar_year % 60


def load_luu_van_rules(path=DEFAULT_RULE_PATH):
    with Path(path).open("r", encoding="utf-8") as source:
        return json.load(source)


def generate_luu_van_stars(day, month, year, hour, yearcalc, rules=None):
    rules = rules or load_luu_van_rules()
    key = ",".join(str(value) for value in luu_van_template_key(day, month, year, hour, yearcalc))
    template = rules["templates"].get(key)
    if template is None:
        raise KeyError(f"Luu Van template {key} was not observed in the rule dataset")
    return template