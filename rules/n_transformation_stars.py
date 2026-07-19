import json
from datetime import date, timedelta
from pathlib import Path

from manual_tools.vietnamese_lunar import solar_to_lunar


DEFAULT_RULE_PATH = Path(__file__).parent / "generated" / "n_transformation_stars.json"


def hour_branch(hour):
    return ((int(hour) + 1) // 2) % 12


def n_transformation_template_key(day, month, year, hour, sex, yearcalc, monthcalc):
    birth_date = date(int(year), int(month), int(day))
    if int(hour) == 23:
        birth_date += timedelta(days=1)
    lunar_day, lunar_month, lunar_year, lunar_leap = solar_to_lunar(
        birth_date.day, birth_date.month, birth_date.year
    )
    return (
        int(yearcalc) % 60,
        int(monthcalc),
        lunar_year % 60,
        int(sex),
        lunar_day,
        lunar_month,
        lunar_leap,
        hour_branch(hour),
    )


def load_n_transformation_rules(path=DEFAULT_RULE_PATH):
    with Path(path).open("r", encoding="utf-8") as source:
        return json.load(source)


def generate_n_transformation_stars(day, month, year, hour, sex, yearcalc, monthcalc, rules=None):
    rules = rules or load_n_transformation_rules()
    key = ",".join(
        str(value)
        for value in n_transformation_template_key(day, month, year, hour, sex, yearcalc, monthcalc)
    )
    template = rules["templates"].get(key)
    if template is None:
        raise KeyError(f"N transformation template {key} was not observed in the rule dataset")
    return template