from enum import StrEnum, auto, unique


@unique
class ErrorStatus(StrEnum):
    CHECKING = auto()
    BOT_350 = auto()
    BOT_800 = auto()
    BOT_1300 = auto()
    BOT_5000 = auto()
    FAMILY_VIEW_100 = auto()
    HUB = auto()
    TRADE_BAN = auto()
    BOT_ANTI_KT = auto()
    DOUBLE_SUBSTITUTION = auto()
    SUCCESS = auto()
