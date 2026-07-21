from .major_stars import generate_major_stars
from .natal_auxiliary_stars import generate_natal_auxiliary_stars
from .van_xuong_van_khuc_stars import generate_van_xuong_van_khuc_stars
from .year_branch_rotation_stars import generate_year_branch_rotation_stars


MAJOR_STAR_IDS = {
    "cu_mon": {15, 136, 177, 182},
    "liem_trinh": {20, 141, 152, 172},
    "pha_quan": {118, 142, 183, 188},
    "tham_lang": {54, 135, 157, 184},
    "thien_co": {110, 144, 158, 166},
    "thien_luong": {35, 145, 171, 180},
    "thien_dong": {67, 164, 178, 190},
    "thai_duong": {129, 162, 170, 185},
    "thai_am": {77, 163, 179, 186},
    "tu_vi": {102, 147, 181, 187},
    "vu_khuc": {92, 161, 174, 189},
}
NATAL_STAR_IDS = {
    **MAJOR_STAR_IDS,
    "ta_phu": {0},
    "huu_bat": {55},
    "van_xuong": {45, 194},
    "van_khuc": {79, 191},
}

# Each row is LN.Loc, LN.Quyen, LN.Khoa, LN.Ki for yearcalc % 10.
ANNUAL_TRANSFORMATIONS = (
    ("thai_duong", "vu_khuc", "thai_am", "thien_dong"),
    ("cu_mon", "thai_duong", "van_khuc", "van_xuong"),
    ("thien_luong", "tu_vi", "ta_phu", "vu_khuc"),
    ("pha_quan", "cu_mon", "thai_am", "tham_lang"),
    ("liem_trinh", "pha_quan", "vu_khuc", "thai_duong"),
    ("thien_co", "thien_luong", "tu_vi", "thai_am"),
    ("thien_dong", "thien_co", "van_xuong", "liem_trinh"),
    ("thai_am", "thien_dong", "thien_co", "cu_mon"),
    ("tham_lang", "thai_am", "huu_bat", "thien_co"),
    ("vu_khuc", "tham_lang", "thien_luong", "van_khuc"),
)


def _slot_for_star(templates, candidate_ids, name):
    slots = [
        slot
        for slot in range(12)
        if any(candidate_ids.intersection(template[slot]) for template in templates)
    ]
    if len(slots) != 1:
        raise ValueError(f"Expected one physical slot for {name}, found {slots}")
    return slots[0]


def generate_luu_nien_transformation_stars(day, month, year, hour, sex, yearcalc, rules=None):
    """Generate annual transformations from the viewing year's heavenly stem."""
    del rules
    natal_templates = (
        generate_major_stars(day, month, year, hour),
        generate_natal_auxiliary_stars(sex, day, month, year, hour),
        generate_van_xuong_van_khuc_stars(day, month, year, hour),
        generate_year_branch_rotation_stars(day, month, year, hour),
    )

    loc_name, quyen_name, khoa_name, ki_name = ANNUAL_TRANSFORMATIONS[int(yearcalc) % 10]
    slots = {
        name: _slot_for_star(natal_templates, NATAL_STAR_IDS[name], name)
        for name in {loc_name, quyen_name, khoa_name, ki_name}
    }
    template = {"left_stars": [[] for _ in range(12)], "right_stars": [[] for _ in range(12)]}
    template["left_stars"][slots[loc_name]].append(8)
    template["left_stars"][slots[quyen_name]].append(122)
    template["left_stars"][slots[khoa_name]].append(83)
    template["right_stars"][slots[ki_name]].append(53)
    return template