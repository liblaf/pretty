from collections.abc import Generator
from typing import Any

from rich.repr import RichReprResult

from liblaf.pretty._prelude import ContainerSpec, PrettyBuilder

from .._registry import registry
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
            match item:
                case (str() | None as name, value, default):
                    if builder.options.hide_defaults and value is default:
                        continue
                    yield name, value
                case (str() | None as name, value):
                    yield name, value
                case value:
                    yield None, value

    return builder.object(filter_fields(builder, field_generator()), referable=True)
