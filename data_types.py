from dataclasses import dataclass, asdict


class StarData(int):
    @property
    def id(self):
        return int(self)

@dataclass
class PalaceData:
    major_stars: list[StarData]
    left_stars: list[StarData]
    right_stars: list[StarData]

@dataclass
class ChartData:
    palaces: list[PalaceData]

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> 'ChartData':
        # Reconstructs from dict if needed
        palaces = [
            PalaceData(
                major_stars=[StarData(**s) for s in p['major_stars']],
                left_stars=[StarData(**s) for s in p['left_stars']],
                right_stars=[StarData(**s) for s in p['right_stars']]
            ) for p in data['palaces']
        ]
        return cls(palaces=palaces)
    
@dataclass
class InputData:
    {
        "name": "", 
        "sex": "1", 
        "day": "27", 
        "month": "3", 
        "year": "1934", 
        "caltype": "1", 
        "hour": "12", 
        "minute": "0", 
        "yearcalc": "2071", 
        "monthcalc": "10", 
        "timezone": "235", 
        "timezoneOption": "1", 
        "solasocanlap": "1", 
        "tuychonthangnhuan": "1", 
        "submitted": "TRUE", 
        "submitcolor": "Lập lá số màu"
    }