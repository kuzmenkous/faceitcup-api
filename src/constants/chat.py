from enum import StrEnum, auto, unique


@unique
class AuthorType(StrEnum):
    CUSTOMER = auto()
    ADMIN = auto()


@unique
class NotificationType(StrEnum):
    CUSTOMER_ROOM_CONNECTION_UPDATE = auto()
    ROOM_MESSAGES_COUNT_UPDATE = auto()
