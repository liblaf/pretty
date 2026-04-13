import enum
from typing import Any


class _TruncatedType(enum.Enum):
    TRUNCATED = enum.auto()


TRUNCATED: Any = _TruncatedType.TRUNCATED
