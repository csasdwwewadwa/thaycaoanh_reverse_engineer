import json
from pathlib import Path


DEFAULT_RULE_PATH = Path(__file__).parent / "generated" / "dai_van_transformation_stars.json"


def dai_van_transformation_template_key(day, month, year, hour, sex, yearcalc, monthcalc):
    return (
        int(sex),
        int(day),
        int(month),
        int(year),
        int(hour),
        int(yearcalc),
        int(monthcalc),
    )


def load_dai_van_transformation_rules(path=DEFAULT_RULE_PATH):
    with Path(path).open("r", encoding="utf-8") as source:
        return json.load(source)


def generate_dai_van_transformation_stars(day, month, year, hour, sex, yearcalc, monthcalc, rules=None):
    rules = rules or load_dai_van_transformation_rules()
    key = ",".join(
        str(value)
        for value in dai_van_transformation_template_key(day, month, year, hour, sex, yearcalc, monthcalc)
    )
    template = rules["templates"].get(key)
    if template is None:
        raise KeyError(f"Dai Van transformation template {key} was not observed in the rule dataset")
    return template