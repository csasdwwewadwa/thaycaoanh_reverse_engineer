import json
from pathlib import Path


DEFAULT_RULE_PATH = Path(__file__).parent / "generated" / "hour_brightness_stars.json"


def hour_branch(hour):
    return ((int(hour) + 1) // 2) % 12


def load_hour_brightness_rules(path=DEFAULT_RULE_PATH):
    with Path(path).open("r", encoding="utf-8") as source:
        return json.load(source)


def generate_hour_brightness_stars(hour, rules=None):
    rules = rules or load_hour_brightness_rules()
    key = str(hour_branch(hour))
    template = rules["templates"].get(key)
    if template is None:
        raise KeyError(f"Hour-brightness template for hour branch {key} was not observed")
    return template