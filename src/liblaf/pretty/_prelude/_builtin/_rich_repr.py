from collections.abc import Generator
from typing import Any

from rich.repr import RichReprResult

from .. import ContainerSpec, PrettyBuilder

from ..._trace._registry import registry
from ._helpers import filter_fields


@registry.register_fallback
def _trace_rich_repr(obj: Any, builder: PrettyBuilder) -> ContainerSpec | None:
    if not hasattr(obj, "__rich_repr__"):
        return None
    result: RichReprResult | None = obj.__rich_repr__()
    if result is None:
        return None

    def field_generator() -> Generator[tuple[str | None, Any]]:
        for item in result:
            parsed = _parse_rich_repr_item(item)
            if parsed is None:
                yield None, item
                continue
            name, value, default = parsed
            if builder.options.hide_defaults and value is default:
                continue
            yield name, value

    return builder.object(filter_fields(builder, field_generator()), referable=True)


def _parse_rich_repr_item(
    item: Any,
) -> tuple[str | None, Any, object] | None:
    if not isinstance(item, tuple):
        return None
    if len(item) == 2 and isinstance(item[0], str | type(None)):
        name, value = item
        return name, value, object()
    if len(item) == 3 and isinstance(item[0], str | type(None)):
        name, value, default = item
        return name, value, default
    return None
