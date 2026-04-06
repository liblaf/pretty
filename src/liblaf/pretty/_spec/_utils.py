import enum
from collections.abc import Iterable
from typing import Any


class MissingType(enum.Enum):
    MISSING = enum.auto()


MISSING: Any = MissingType.MISSING


def truncate[T](iterable: Iterable[T], max_len: int | None, fill_value: T) -> list[T]:
    if max_len is None:
        return list(iterable)
    result: list[T] = []
    for i, item in enumerate(iterable):
        if i >= max_len:
            result.append(fill_value)
            break
        result.append(item)
    return result
