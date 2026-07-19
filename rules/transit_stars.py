import json
from pathlib import Path


DEFAULT_RULE_PATH = Path(__file__).parent / "generated" / "transit_stars.json"


def view_year_stem(yearcalc):
    return int(yearcalc) % 10


def view_year_branch(yearcalc):
    return int(yearcalc) % 12


def load_transit_rules(path=DEFAULT_RULE_PATH):
    with Path(path).open("r", encoding="utf-8") as source:
        return json.load(source)


def generate_transit_stars(yearcalc, rules=None):
    rules = rules or load_transit_rules()
    template = rules["templates"].get(str(int(yearcalc) % 60))
    if template is None:
        raise KeyError(f"Transit template for viewing-year cycle {int(yearcalc) % 60} was not observed")
    return template


def generate_transit_star_locations(yearcalc, rules=None):
    rules = rules or load_transit_rules()
    output = [[] for _ in range(12)]
    for rule in rules["rules"]:
        selector = rule["selector"]
        if selector == "view_year_stem":
            key = view_year_stem(yearcalc)
        elif selector == "view_year_branch":
            key = view_year_branch(yearcalc)
        else:
            raise ValueError(f"Unsupported transit selector {selector!r}")
        palace_index = rule["palace_by_key"].get(str(key))
        if palace_index is None:
            raise KeyError(f"Transit rule {rule['id']} has no placement for key {key}")
        output[palace_index].append(rule["id"])
    return output