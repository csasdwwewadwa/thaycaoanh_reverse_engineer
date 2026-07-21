from .luu_nien_transformation_stars import (
    ANNUAL_TRANSFORMATIONS,
    NATAL_STAR_IDS,
    _slot_for_star,
)
from .major_stars import generate_major_stars
from .natal_auxiliary_stars import generate_natal_auxiliary_stars
from .van_xuong_van_khuc_stars import generate_van_xuong_van_khuc_stars
from .year_branch_rotation_stars import generate_year_branch_rotation_stars


def monthly_transformation_row(yearcalc, monthcalc):
    return (int(monthcalc) - 1 + 2 * (int(yearcalc) % 10 - 1)) % 10


def generate_n_transformation_stars(day, month, year, hour, sex, yearcalc, monthcalc, rules=None):
    del rules
    natal_templates = (
        generate_major_stars(day, month, year, hour),
        generate_natal_auxiliary_stars(sex, day, month, year, hour),
        generate_van_xuong_van_khuc_stars(day, month, year, hour),
        generate_year_branch_rotation_stars(day, month, year, hour),
    )
    loc_name, quyen_name, khoa_name, ki_name = ANNUAL_TRANSFORMATIONS[
        monthly_transformation_row(yearcalc, monthcalc)
    ]
    slots = {
        name: _slot_for_star(natal_templates, NATAL_STAR_IDS[name], name)
        for name in {loc_name, quyen_name, khoa_name, ki_name}
    }
    template = {"left_stars": [[] for _ in range(12)], "right_stars": [[] for _ in range(12)]}
    template["left_stars"][slots[loc_name]].append(82)
    template["left_stars"][slots[quyen_name]].append(47)
    template["left_stars"][slots[khoa_name]].append(31)
    template["right_stars"][slots[ki_name]].append(91)
    return template