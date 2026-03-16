from collections.abc import Generator
from typing import Any

from rich.repr import RichReprResult

from liblaf.pretty._lower import Traced, TracedContainer, TracedItem, TracedReference

from ._base import TraceContext
from ._registry import trace
from ._utils import trace_dataclass


@trace.register_func
def _trace_rich_repr(obj: Any, ctx: TraceContext) -> Traced | None:
    if not hasattr(obj, "__rich_repr__"):
        return None
    result: RichReprResult | None = obj.__rich_repr__()
    if not result:
        return None
    if ctx.visit(obj):
        return TracedReference.new(obj)

    def field_generator() -> Generator[tuple[str | None, Any]]:
        for item in result:
            match item:
                case (str() | None as name, value, default):
                    if ctx.config.hide_defaults and value is default:
                        continue
                    yield name, value
                case (str() | None as name, value):
                    yield name, value
                case value:
                    yield None, value

    children: list[TracedItem] = trace_dataclass(ctx, field_generator())
    return TracedContainer(
        children=children,
        cls=type(obj),
        obj_id=id(obj),
        open_brace="(",
        close_brace=")",
    )
