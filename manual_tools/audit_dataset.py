import argparse
import hashlib
import json
import sqlite3
from collections import Counter
from pathlib import Path


INPUT_FIELDS = (
    "sex",
    "day",
    "month",
    "year",
    "caltype",
    "hour",
    "minute",
    "yearcalc",
    "monthcalc",
    "timezone",
    "timezoneOption",
    "solasocanlap",
    "tuychonthangnhuan",
)
STAR_GROUPS = ("major_stars", "left_stars", "right_stars")


def canonical_input(input_data):
    return tuple(str(input_data.get(field, "")) for field in INPUT_FIELDS)


def canonical_output(palaces):
    return tuple(
        tuple(tuple(int(star_id) for star_id in palace.get(group, ())) for group in STAR_GROUPS)
        for palace in palaces
    )


def digest(value):
    payload = json.dumps(value, separators=(",", ":"), ensure_ascii=True).encode("ascii")
    return hashlib.sha256(payload).digest()


def percentile(counter, fraction):
    if not counter:
        return None
    threshold = sum(counter.values()) * fraction
    cumulative = 0
    for value in sorted(counter):
        cumulative += counter[value]
        if cumulative >= threshold:
            return value
    return max(counter)


class Audit:
    def __init__(self, connection, max_samples):
        self.connection = connection
        self.max_samples = max_samples
        self.rows = 0
        self.valid_charts = 0
        self.invalid_json = 0
        self.invalid_palace_count = 0
        self.duplicate_inputs = 0
        self.conflicting_inputs = 0
        self.conflict_samples = []
        self.duplicate_star_charts = 0
        self.duplicate_star_samples = []
        self.star_appearances = Counter()
        self.star_chart_appearances = Counter()
        self.star_palace_masks = Counter()
        self.star_sources = {}
        self.stars_per_chart = Counter()
        self.stars_per_palace = Counter()
        self.major_templates = Counter()

    def audit_chart(self, line_number, item):
        input_data = item["input_data"]
        palaces = item["output_chart"]["palaces"]
        if len(palaces) != 12:
            self.invalid_palace_count += 1
            return

        self.valid_charts += 1
        output = canonical_output(palaces)
        self._audit_duplicate_input(line_number, canonical_input(input_data), output)

        seen = Counter()
        chart_star_count = 0
        major_template = []
        for palace_index, palace in enumerate(palaces):
            palace_count = 0
            major_template.append(tuple(int(value) for value in palace.get("major_stars", ())))
            for group in STAR_GROUPS:
                for raw_star_id in palace.get(group, ()):
                    star_id = int(raw_star_id)
                    seen[star_id] += 1
                    chart_star_count += 1
                    palace_count += 1
                    self.star_appearances[star_id] += 1
                    self.star_palace_masks[star_id] |= 1 << palace_index
                    self.star_sources.setdefault(star_id, Counter())[group] += 1
            self.stars_per_palace[palace_count] += 1

        self.stars_per_chart[chart_star_count] += 1
        self.major_templates[tuple(major_template)] += 1
        for star_id in seen:
            self.star_chart_appearances[star_id] += 1

        duplicates = sorted(star_id for star_id, count in seen.items() if count > 1)
        if duplicates:
            self.duplicate_star_charts += 1
            if len(self.duplicate_star_samples) < self.max_samples:
                self.duplicate_star_samples.append({"line": line_number, "star_ids": duplicates})

    def _audit_duplicate_input(self, line_number, input_value, output_value):
        input_hash = digest(input_value)
        output_hash = digest(output_value)
        row = self.connection.execute(
            "SELECT output_hash, first_line FROM seen_inputs WHERE input_hash = ?",
            (input_hash,),
        ).fetchone()
        if row is None:
            self.connection.execute(
                "INSERT INTO seen_inputs(input_hash, output_hash, first_line) VALUES (?, ?, ?)",
                (input_hash, output_hash, line_number),
            )
            return

        self.duplicate_inputs += 1
        if row[0] != output_hash:
            self.conflicting_inputs += 1
            if len(self.conflict_samples) < self.max_samples:
                self.conflict_samples.append(
                    {"first_line": row[1], "conflicting_line": line_number}
                )

    def report(self):
        star_ids = sorted(self.star_appearances)
        inconsistent_sources = {
            str(star_id): dict(sorted(self.star_sources[star_id].items()))
            for star_id in star_ids
            if len(self.star_sources[star_id]) != 1
        }
        never_seen = sorted(set(range(195)) - set(star_ids))
        star_stats = {
            str(star_id): {
                "appearances": self.star_appearances[star_id],
                "charts": self.star_chart_appearances[star_id],
                "chart_frequency": self.star_chart_appearances[star_id] / self.valid_charts,
                "possible_palaces": [
                    palace for palace in range(12) if self.star_palace_masks[star_id] & (1 << palace)
                ],
                "sources": dict(sorted(self.star_sources[star_id].items())),
            }
            for star_id in star_ids
        }
        top_templates = [
            {"count": count, "palaces": template}
            for template, count in self.major_templates.most_common(20)
        ]
        return {
            "rows_read": self.rows,
            "valid_charts": self.valid_charts,
            "invalid_json_rows": self.invalid_json,
            "invalid_palace_count_rows": self.invalid_palace_count,
            "unique_inputs": self.valid_charts - self.duplicate_inputs,
            "duplicate_inputs": self.duplicate_inputs,
            "conflicting_duplicate_inputs": self.conflicting_inputs,
            "conflict_samples": self.conflict_samples,
            "charts_with_duplicate_star_ids": self.duplicate_star_charts,
            "duplicate_star_samples": self.duplicate_star_samples,
            "observed_star_count": len(star_ids),
            "observed_star_id_range": [min(star_ids), max(star_ids)] if star_ids else None,
            "never_seen_star_ids_in_expected_range": never_seen,
            "stars_with_inconsistent_source_columns": inconsistent_sources,
            "stars_per_chart": {
                "min": min(self.stars_per_chart) if self.stars_per_chart else None,
                "median": percentile(self.stars_per_chart, 0.5),
                "p95": percentile(self.stars_per_chart, 0.95),
                "max": max(self.stars_per_chart) if self.stars_per_chart else None,
            },
            "stars_per_palace": {
                "min": min(self.stars_per_palace) if self.stars_per_palace else None,
                "median": percentile(self.stars_per_palace, 0.5),
                "p95": percentile(self.stars_per_palace, 0.95),
                "max": max(self.stars_per_palace) if self.stars_per_palace else None,
            },
            "unique_major_templates": len(self.major_templates),
            "top_major_templates": top_templates,
            "stars": star_stats,
        }


def create_connection(database_path):
    connection = sqlite3.connect(database_path)
    connection.execute("PRAGMA journal_mode=WAL")
    connection.execute("PRAGMA synchronous=NORMAL")
    connection.execute(
        """
        CREATE TABLE IF NOT EXISTS seen_inputs (
            input_hash BLOB PRIMARY KEY,
            output_hash BLOB NOT NULL,
            first_line INTEGER NOT NULL
        ) WITHOUT ROWID
        """
    )
    connection.execute("DELETE FROM seen_inputs")
    return connection


def run(args):
    connection = create_connection(args.database)
    audit = Audit(connection, args.max_samples)
    try:
        with args.dataset.open("r", encoding="utf-8") as source:
            for line_number, line in enumerate(source, 1):
                if args.limit and audit.rows >= args.limit:
                    break
                if not line.strip():
                    continue
                audit.rows += 1
                try:
                    audit.audit_chart(line_number, json.loads(line))
                except (json.JSONDecodeError, KeyError, TypeError, ValueError):
                    audit.invalid_json += 1
                if audit.rows % args.progress_every == 0:
                    connection.commit()
                    print(f"Audited {audit.rows:,} rows", flush=True)
        connection.commit()
    finally:
        connection.close()

    report = audit.report()
    args.report.write_text(
        json.dumps(report, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print(json.dumps({key: report[key] for key in (
        "rows_read",
        "valid_charts",
        "duplicate_inputs",
        "conflicting_duplicate_inputs",
        "charts_with_duplicate_star_ids",
        "observed_star_count",
        "unique_major_templates",
    )}, indent=2))
    print(f"Full report: {args.report}")


def parse_args():
    parser = argparse.ArgumentParser(description="Audit scraped chart determinism and invariants.")
    parser.add_argument("dataset", type=Path, nargs="?", default=Path("metadata copy.jsonl"))
    parser.add_argument("--database", type=Path, default=Path("dataset_audit.sqlite3"))
    parser.add_argument("--report", type=Path, default=Path("dataset_audit.json"))
    parser.add_argument("--limit", type=int, default=0, help="Stop after this many non-empty rows.")
    parser.add_argument("--progress-every", type=int, default=10_000)
    parser.add_argument("--max-samples", type=int, default=20)
    return parser.parse_args()


if __name__ == "__main__":
    run(parse_args())