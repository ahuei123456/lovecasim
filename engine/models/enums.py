from enum import IntEnum
from typing import Any, List


class CardType(IntEnum):
    """Card types in the game"""

    MEMBER = 0
    LIVE = 1
    ENERGY = 2


class HeartColor(IntEnum):
    """Heart/color types (6 colors + any + rainbow)"""

    PINK = 0
    RED = 1
    YELLOW = 2
    GREEN = 3
    BLUE = 4
    PURPLE = 5
    ANY = 6  # Colorless requirement
    RAINBOW = 7  # Can be any color


class Area(IntEnum):
    """Member areas on stage"""

    LEFT = 0
    CENTER = 1
    RIGHT = 2


class Group(IntEnum):
    """Card Groups (Series/Schools)"""

    MUSE = 0
    AQOURS = 1
    NIJIGASAKI = 2
    LIELLA = 3
    HASUNOSORA = 4
    OTHER = 99

    @classmethod
    def from_japanese_name(cls, name: str) -> "Group":
        name = name.strip()
        if "ラブライブ！" == name or "μ's" in name:
            return cls.MUSE
        if "サンシャイン" in name or "Aqours" in name:
            return cls.AQOURS
        if "虹ヶ咲" in name:
            return cls.NIJIGASAKI
        if "スーパースター" in name or "Liella" in name:
            return cls.LIELLA
        if "蓮ノ空" in name:
            return cls.HASUNOSORA
        return cls.OTHER


class Unit(IntEnum):
    """Card Units"""

    PRINTEMPS = 0
    LILY_WHITE = 1
    BIBI = 2
    CYARON = 3
    AZALEA = 4
    GUILTY_KISS = 5
    DIVER_DIVA = 6
    A_ZU_NA = 7
    QU4RTZ = 8
    R3BIRTH = 9
    CATCHU = 10
    KALEIDOSCORE = 11
    SYNCRISE = 12
    CERISE_BOUQUET = 13
    DOLLCHESTRA = 14
    MIRA_CRA_PARK = 15
    EDEL_NOTE = 16
    OTHER = 99

    @classmethod
    def from_japanese_name(cls, name: str) -> "Unit":
        name = name.strip()
        name_lower = name.lower()
        if "printemps" in name_lower:
            return cls.PRINTEMPS
        if "lily white" in name_lower or "lilywhite" in name_lower:
            return cls.LILY_WHITE
        if "bibi" in name_lower:
            return cls.BIBI
        if "cyaron" in name_lower or "cyaron！" in name_lower:
            return cls.CYARON
        if "azalea" in name_lower:
            return cls.AZALEA
        if "guilty kiss" in name_lower or "guiltykiss" in name_lower:
            return cls.GUILTY_KISS
        if "diverdiva" in name_lower:
            return cls.DIVER_DIVA
        if "azuna" in name_lower or "a・zu・na" in name_lower:
            return cls.A_ZU_NA
        if "qu4rtz" in name_lower:
            return cls.QU4RTZ
        if "r3birth" in name_lower:
            return cls.R3BIRTH
        if "catchu" in name_lower:
            return cls.CATCHU
        if "kaleidoscore" in name_lower:
            return cls.KALEIDOSCORE
        if "5yncri5e" in name_lower:
            return cls.SYNCRISE
        if "スリーズブーケ" in name:
            return cls.CERISE_BOUQUET
        if "dollchestra" in name_lower:
            return cls.DOLLCHESTRA
        if "みらくらぱーく" in name:
            return cls.MIRA_CRA_PARK
        if "edelnote" in name_lower:
            return cls.EDEL_NOTE
        if not name:
            return cls.OTHER
        return cls.OTHER


def ensure_group_list(v: Any) -> List[Group]:
    """Validator to convert string/single Group to List[Group]"""
    if isinstance(v, list):
        return [g if isinstance(g, Group) else Group.from_japanese_name(str(g)) for g in v]
    if isinstance(v, Group):
        return [v]
    if isinstance(v, str):
        if not v:
            return []
        parts = [p.strip() for p in v.split("\n") if p.strip()]
        return [Group.from_japanese_name(p) for p in parts]
    return []


def ensure_unit_list(v: Any) -> List[Unit]:
    """Validator to convert string/single Unit to List[Unit]"""
    if isinstance(v, list):
        return [u if isinstance(u, Unit) else Unit.from_japanese_name(str(u)) for u in v]
    if isinstance(v, Unit):
        return [v]
    if isinstance(v, str):
        if not v:
            return []
        parts = [p.strip() for p in v.split("\n") if p.strip()]
        return [Unit.from_japanese_name(p) for p in parts]
    return []
