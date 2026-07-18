import math


SYNODIC_MONTH = 29.530588853
NEW_MOON_EPOCH = 2415021.076998695


def julian_day(day, month, year):
    offset = (14 - month) // 12
    adjusted_year = year + 4800 - offset
    adjusted_month = month + 12 * offset - 3
    value = (
        day
        + (153 * adjusted_month + 2) // 5
        + 365 * adjusted_year
        + adjusted_year // 4
        - adjusted_year // 100
        + adjusted_year // 400
        - 32045
    )
    if value < 2299161:
        value = (
            day
            + (153 * adjusted_month + 2) // 5
            + 365 * adjusted_year
            + adjusted_year // 4
            - 32083
        )
    return value


def new_moon_day(index, timezone=7.0):
    centuries = index / 1236.85
    centuries_squared = centuries * centuries
    centuries_cubed = centuries_squared * centuries
    radians = math.pi / 180
    mean_julian_day = (
        2415020.75933
        + SYNODIC_MONTH * index
        + 0.0001178 * centuries_squared
        - 0.000000155 * centuries_cubed
    )
    mean_julian_day += 0.00033 * math.sin((166.56 + 132.87 * centuries - 0.009173 * centuries_squared) * radians)
    sun_anomaly = 359.2242 + 29.10535608 * index - 0.0000333 * centuries_squared - 0.00000347 * centuries_cubed
    moon_anomaly = 306.0253 + 385.81691806 * index + 0.0107306 * centuries_squared + 0.00001236 * centuries_cubed
    latitude_argument = 21.2964 + 390.67050646 * index - 0.0016528 * centuries_squared - 0.00000239 * centuries_cubed
    correction = (
        (0.1734 - 0.000393 * centuries) * math.sin(sun_anomaly * radians)
        + 0.0021 * math.sin(2 * sun_anomaly * radians)
        - 0.4068 * math.sin(moon_anomaly * radians)
        + 0.0161 * math.sin(2 * moon_anomaly * radians)
        - 0.0004 * math.sin(3 * moon_anomaly * radians)
        + 0.0104 * math.sin(2 * latitude_argument * radians)
        - 0.0051 * math.sin((sun_anomaly + moon_anomaly) * radians)
        - 0.0074 * math.sin((sun_anomaly - moon_anomaly) * radians)
        + 0.0004 * math.sin((2 * latitude_argument + sun_anomaly) * radians)
        - 0.0004 * math.sin((2 * latitude_argument - sun_anomaly) * radians)
        - 0.0006 * math.sin((2 * latitude_argument + moon_anomaly) * radians)
        + 0.0010 * math.sin((2 * latitude_argument - moon_anomaly) * radians)
        + 0.0005 * math.sin((2 * moon_anomaly + sun_anomaly) * radians)
    )
    if centuries < -11:
        delta_t = 0.001 + 0.000839 * centuries + 0.0002261 * centuries_squared - 0.00000845 * centuries_cubed - 0.000000081 * centuries_squared**2
    else:
        delta_t = -0.000278 + 0.000265 * centuries + 0.000262 * centuries_squared
    return math.floor(mean_julian_day + correction - delta_t + 0.5 + timezone / 24)


def sun_longitude(day_number, timezone=7.0):
    centuries = (day_number - 2451545.5 - timezone / 24) / 36525
    centuries_squared = centuries * centuries
    radians = math.pi / 180
    mean_anomaly = 357.52910 + 35999.05030 * centuries - 0.0001559 * centuries_squared - 0.00000048 * centuries_squared * centuries
    mean_longitude = 280.46645 + 36000.76983 * centuries + 0.0003032 * centuries_squared
    correction = (
        (1.914600 - 0.004817 * centuries - 0.000014 * centuries_squared) * math.sin(mean_anomaly * radians)
        + (0.019993 - 0.000101 * centuries) * math.sin(2 * mean_anomaly * radians)
        + 0.000290 * math.sin(3 * mean_anomaly * radians)
    )
    longitude = (mean_longitude + correction) * radians
    return math.floor((longitude % (2 * math.pi)) / math.pi * 6)


def lunar_month_11(year, timezone=7.0):
    off = julian_day(31, 12, year) - 2415021
    index = math.floor(off / SYNODIC_MONTH)
    month_start = new_moon_day(index, timezone)
    if sun_longitude(month_start, timezone) >= 9:
        month_start = new_moon_day(index - 1, timezone)
    return month_start


def leap_month_offset(month_11, timezone=7.0):
    index = math.floor((month_11 - NEW_MOON_EPOCH) / SYNODIC_MONTH + 0.5)
    previous_longitude = sun_longitude(new_moon_day(index + 1, timezone), timezone)
    offset = 2
    while offset < 14:
        longitude = sun_longitude(new_moon_day(index + offset, timezone), timezone)
        if longitude == previous_longitude:
            break
        previous_longitude = longitude
        offset += 1
    return offset - 1


def solar_to_lunar(day, month, year, timezone=7.0):
    day_number = julian_day(day, month, year)
    index = math.floor((day_number - NEW_MOON_EPOCH) / SYNODIC_MONTH)
    month_start = new_moon_day(index + 1, timezone)
    if month_start > day_number:
        month_start = new_moon_day(index, timezone)

    month_11_after = lunar_month_11(year, timezone)
    if month_11_after >= month_start:
        lunar_year = year
        month_11_before = lunar_month_11(year - 1, timezone)
    else:
        lunar_year = year + 1
        month_11_before = month_11_after
        month_11_after = lunar_month_11(year + 1, timezone)

    lunar_day = day_number - month_start + 1
    month_difference = math.floor((month_start - month_11_before) / 29)
    lunar_leap = 0
    lunar_month = month_difference + 11
    if month_11_after - month_11_before > 365:
        leap_difference = leap_month_offset(month_11_before, timezone)
        if month_difference >= leap_difference:
            lunar_month = month_difference + 10
            if month_difference == leap_difference:
                lunar_leap = 1
    if lunar_month > 12:
        lunar_month -= 12
    if lunar_month >= 11 and month_difference < 4:
        lunar_year -= 1
    return lunar_day, lunar_month, lunar_year, lunar_leap