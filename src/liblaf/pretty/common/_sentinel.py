"""Sentinel values used while truncating collections."""

import enum
from typing import Any


class _TruncatedType(enum.Enum):
    """Sentinel enum used to mark truncated output."""

    TRUNCATED = enum.auto()


TRUNCATED: Any = _TruncatedType.TRUNCATED
