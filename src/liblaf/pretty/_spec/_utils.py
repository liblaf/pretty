import enum
from typing import Any


class MissingType(enum.Enum):
    MISSING = enum.auto()


MISSING: Any = MissingType.MISSING
