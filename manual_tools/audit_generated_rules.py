import argparse
import json
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_RULE_DIRECTORY = PROJECT_ROOT / "rules" / "generated"


def audit_rule(path):
    with path.open("r", encoding="utf-8") as source:
        artifact = json.load(source)
    templates = artifact.get("templates", {})
    return {
        "file": path.name,
        "size_mb": round(path.stat().st_size / 1_000_000, 1),
        "template_count": len(templates),
        "template_key": artifact.get("template_key", []),
        "rows_validated": artifact.get("rows_validated"),
    }


def run(rule_directory, minimum_size_mb):
    rule_directory = Path(rule_directory)
    reports = []
    for path in rule_directory.glob("*.json"):
        if path.stat().st_size / 1_000_000 < minimum_size_mb:
            continue
        reports.append(audit_rule(path))

    for report in sorted(reports, key=lambda item: item["size_mb"], reverse=True):
        selector = ", ".join(report["template_key"]) or "<no template key>"
        print(
            f"{report['file']}: {report['size_mb']:.1f} MB; "
            f"{report['template_count']:,} templates; selector=[{selector}]"
        )


def parse_args():
    parser = argparse.ArgumentParser(description="Audit generated rule artifact size and selector state.")
    parser.add_argument("--rule-directory", type=Path, default=DEFAULT_RULE_DIRECTORY)
    parser.add_argument("--minimum-size-mb", type=float, default=1.0)
    return parser.parse_args()


if __name__ == "__main__":
    arguments = parse_args()
    run(arguments.rule_directory, arguments.minimum_size_mb)
