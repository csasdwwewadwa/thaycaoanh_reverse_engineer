import json
from datetime import date, timedelta
from pathlib import Path

from manual_tools.vietnamese_lunar import solar_to_lunar


DEFAULT_RULE_PATH = Path(__file__).parent / "generated" / "van_xuong_van_khuc_stars.json"


def hour_branch(hour):
    return ((int(hour) + 1) // 2) % 12


def van_xuong_van_khuc_template_key(day, month, year, hour):
    birth_date = date(int(year), int(month), int(day))
    if int(hour) == 23:
        birth_date += timedelta(days=1)
    _, lunar_month, _, lunar_leap = solar_to_lunar(
        birth_date.day, birth_date.month, birth_date.year
    )
    return lunar_month, lunar_leap, hour_branch(hour)


def load_van_xuong_van_khuc_rules(path=DEFAULT_RULE_PATH):
    with Path(path).open("r", encoding="utf-8") as source:
        return json.load(source)


def generate_van_xuong_van_khuc_stars(day, month, year, hour, rules=None):
    rules = rules or load_van_xuong_van_khuc_rules()
    key = ",".join(str(value) for value in van_xuong_van_khuc_template_key(day, month, year, hour))
    template = rules["templates"].get(key)
    if template is None:
        raise KeyError(f"Van Xuong/Van Khuc template {key} was not observed in the rule dataset")
    return template