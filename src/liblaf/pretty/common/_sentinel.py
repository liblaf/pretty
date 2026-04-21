
"""Internal sentinel values used during truncation."""

import enum
from typing import Any


class _TruncatedType(enum.Enum):

    TRUNCATED = enum.auto()


TRUNCATED: Any = _TruncatedType.TRUNCATED
"""Sentinel inserted when a container is truncated by the active limits."""
