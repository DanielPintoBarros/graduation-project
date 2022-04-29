import enum


class UserAccessLevelEnum(enum.Enum):
    ADMIN = "ADMIN"
    REGISTER = "REGISTER"
    OPERATOR = "OPERATOR"
    VIEWER = "VIEWER"


class RegisterTypeEnum(enum.Enum):
    ENERGY = "ENERGY"
    WATER = "WATER"


class AlarmSeverityEnum(enum.Enum):
    WARNING = "WARNING"
    CRITICAL = "CRITICAL"


class AlarmStatusEnum(enum.Enum):
    ACTIVE = "ACTIVE"
    RESOLVED = "RESOLVED"
