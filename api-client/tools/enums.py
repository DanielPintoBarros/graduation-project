import enum


class UserAccessLevelEnum(enum.Enum):
    ADMIN = "ADMIN"
    REGISTER = "REGISTER"
    OPERATOR = "OPERATOR"
    VIEWER = "VIEWER"


class RegisterTypeEnum(enum.Enum):
    ENERGY1 = "ENERGY1"
    ENERGY2 = "ENERGY2"
    ENERGY3 = "ENERGY3"
    WATER = "WATER"


class AlarmSeverityEnum(enum.Enum):
    WARNING = "WARNING"
    CRITICAL = "CRITICAL"


class AlarmStatusEnum(enum.Enum):
    ACTIVE = "ACTIVE"
    RESOLVED = "RESOLVED"
