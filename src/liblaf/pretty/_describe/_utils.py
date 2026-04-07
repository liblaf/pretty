from collections.abc import Generator, Iterable

from liblaf.pretty._const import COMMA, SPACE
from liblaf.pretty._spec import SpecItem


def add_separators(items: Iterable[SpecItem]) -> list[SpecItem]:
    items: list[SpecItem] = list(items)
    for i, item in enumerate(items):
        if i > 0:
            item.prefix = SPACE
        if i < len(items) - 1:
            item.suffix = COMMA
    return items


def truncate[T](iterable: Iterable[T], max_len: int | None, fill: T) -> Generator[T]:
    if max_len is None:
        yield from iterable
    else:
        for i, item in enumerate(iterable):
            if i >= max_len:
                yield fill
                break
            yield item
