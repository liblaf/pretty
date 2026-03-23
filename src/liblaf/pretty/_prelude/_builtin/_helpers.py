from collections.abc import Iterable, Iterator

from .. import ItemSpec, PrettyBuilder


def truncate_sequence(
    builder: PrettyBuilder, sequence: Iterable[object], limit: int
) -> tuple[ItemSpec, ...]:
    items: list[ItemSpec] = []
    for i, item in enumerate(sequence):
        if i >= limit:
            items.append(builder.value(builder.ellipsis()))
            break
        items.append(builder.value(item))
    return tuple(items)


def truncate_mapping(
    builder: PrettyBuilder, mapping: Iterable[tuple[object, object]], limit: int
) -> tuple[ItemSpec, ...]:
    items: list[ItemSpec] = []
    for i, (key, value) in enumerate(mapping):
        if i >= limit:
            items.append(builder.value(builder.ellipsis()))
            break
        items.append(builder.entry(key, value))
    return tuple(items)


def filter_fields(
    builder: PrettyBuilder, fields: Iterable[tuple[str | None, object]]
) -> Iterator[ItemSpec]:
    for name, value in fields:
        if name is None:
            yield builder.value(value)
        else:
            yield builder.field(name, value)
