from collections.abc import Callable, Iterable
from typing import Any

import rules


LEFT_STAR_ORDER = (
    16, 132, 111, 176, 133, 155, 78, 151, 22, 93, 104, 45, 79, 191,
    194, 55, 0, 36, 149, 119, 120, 68, 1, 69, 94, 37, 112, 56, 70, 23,
    95, 80, 57, 24, 2, 25, 26, 81, 113, 114, 38, 58, 46, 96, 27, 71,
    28, 59, 3, 29, 4, 105, 121, 5, 17, 6, 60, 61, 7, 30, 8, 82, 97,
    122, 47, 9, 83, 31,
)
RIGHT_STAR_ORDER = (
    84, 123, 10, 11, 130, 143, 192, 193, 72, 106, 134, 32, 62, 156,
    137, 85, 18, 115, 165, 124, 125, 12, 126, 168, 140, 169, 138, 39,
    48, 146, 154, 98, 160, 33, 49, 127, 19, 40, 86, 116, 73, 107, 41,
    74, 99, 63, 108, 64, 50, 100, 87, 51, 75, 42, 88, 13, 128, 76, 65,
    89, 14, 34, 43, 52, 66, 101, 109, 117, 90, 53, 91,
)

LEFT_STAR_RANK = {star_id: rank for rank, star_id in enumerate(LEFT_STAR_ORDER)}
RIGHT_STAR_RANK = {star_id: rank for rank, star_id in enumerate(RIGHT_STAR_ORDER)}


def _auxiliary_generators(
    sex: int,
    day: int,
    month: int,
    year: int,
    hour: int,
    yearcalc: int,
    monthcalc: int,
) -> Iterable[tuple[str, Any]]:
    yield "hour_brightness", rules.generate_hour_brightness_stars(hour)
    yield "hao_brightness", rules.generate_hao_brightness_stars(day, month, year, hour, sex)
    yield "four_brightness_families", rules.generate_four_brightness_families_stars(
        day, month, year, hour, sex
    )
    yield "thien_dieu_brightness", rules.generate_thien_dieu_brightness_stars(
        day, month, year, hour, sex
    )
    yield "tang_mon_brightness", rules.generate_tang_mon_brightness_stars(
        day, month, year, hour, sex
    )
    yield "eleven_star_annual", rules.generate_eleven_star_annual_stars(day, month, year, hour, sex)
    yield "luu_nien_transformation", rules.generate_luu_nien_transformation_stars(
        day, month, year, hour, sex, yearcalc
    )
    yield "n_transformation", rules.generate_n_transformation_stars(
        day, month, year, hour, sex, yearcalc, monthcalc
    )
    yield "dai_van_transformation", rules.generate_dai_van_transformation_stars(
        day, month, year, hour, sex, yearcalc, monthcalc
    )
    yield "luu_ha", rules.generate_luu_ha_stars(day, month, year, hour)
    yield "am_sat", rules.generate_am_sat_stars(day, month, year, hour)
    yield "luu_van", rules.generate_luu_van_stars(day, month, year, hour, yearcalc)
    yield "hoa_linh", rules.generate_hoa_linh_stars(day, month, year, hour, sex)
    yield "hoa_transformation", rules.generate_hoa_transformation_stars(day, month, year, hour, sex)
    yield "day_rotation", rules.generate_day_rotation_stars(day, month, year, hour)
    yield "kinh_duong_da_la", rules.generate_kinh_duong_da_la_stars(day, month, year, hour)
    yield "loc_ton_bac_sy", rules.generate_loc_ton_bac_sy_stars(day, month, year, hour, sex)
    yield "natal_auxiliary", rules.generate_natal_auxiliary_stars(sex, day, month, year, hour)
    yield "right_constrained_natal", rules.generate_right_constrained_natal_stars(
        day, month, year, hour, sex
    )
    yield "thien_khoi_thien_viet", rules.generate_thien_khoi_thien_viet_stars(day, month, year, hour)
    yield "thien_quan_thien_phuc", rules.generate_thien_quan_thien_phuc_stars(day, month, year, hour)
    yield "thien_tru_duong_phu", rules.generate_thien_tru_duong_phu_stars(day, month, year, hour)
    yield "thien_ma", rules.generate_thien_ma_stars(day, month, year, hour)
    yield "thai_tue_series", rules.generate_thai_tue_series_stars(day, month, year, hour, sex)
    yield "transit", rules.generate_transit_stars(yearcalc)
    yield "van_xuong_van_khuc", rules.generate_van_xuong_van_khuc_stars(day, month, year, hour)
    yield "year_branch_rotation", rules.generate_year_branch_rotation_stars(day, month, year, hour)


def _add_template(
    chart: dict[str, list[list[int]]], template: Any, source: str) -> None:
    templates = template.items() if isinstance(template, dict) else ((None, template),)
    for declared_column, slots in templates:
        if declared_column is not None and declared_column not in ("left_stars", "right_stars"):
            raise ValueError(f"{source} returned unexpected column {declared_column!r}")
        if len(slots) != 12:
            raise ValueError(f"{source} returned {len(slots)} slots instead of 12")
        for slot, stars in enumerate(slots):
            for raw_star_id in stars:
                star_id = int(raw_star_id)
                column = declared_column or (
                    "left_stars" if star_id in LEFT_STAR_RANK else "right_stars"
                    if star_id in RIGHT_STAR_RANK else None
                )
                if column is None:
                    raise ValueError(f"{source} emitted unclassified star {star_id}")
                if star_id in chart[column][slot]:
                    raise ValueError(
                        f"duplicate star {star_id} in {column} slot {slot} from {source}"
                    )
                chart[column][slot].append(star_id)


def generate_chart(
    sex: int,
    day: int,
    month: int,
    year: int,
    hour: int,
    minute: int,
    yearcalc: int,
    monthcalc: int,
    **_ignored: Any,
) -> dict[str, list[list[int]]]:
    """Generate the three exact physical output columns for one chart input."""
    del minute
    numeric = {
        name: int(value)
        for name, value in {
            "sex": sex,
            "day": day,
            "month": month,
            "year": year,
            "hour": hour,
            "yearcalc": yearcalc,
            "monthcalc": monthcalc,
        }.items()
    }
    chart = {column: [[] for _ in range(12)] for column in ("major_stars", "left_stars", "right_stars")}
    chart["major_stars"] = rules.generate_major_stars(
        numeric["day"], numeric["month"], numeric["year"], numeric["hour"]
    )

    for source, template in _auxiliary_generators(**numeric):
        _add_template(chart, template, source)

    for column, ranks in (("left_stars", LEFT_STAR_RANK), ("right_stars", RIGHT_STAR_RANK)):
        for stars in chart[column]:
            stars.sort(key=ranks.__getitem__)
    return chart