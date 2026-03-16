from collections.abc import Generator
from typing import Any

import fieldz

from liblaf.pretty._lower import Traced, TracedContainer, TracedItem, TracedReference

from ._base import TraceContext
from ._registry import trace
from ._utils import trace_dataclass


@trace.register_func
def _trace_fieldz(obj: Any, ctx: TraceContext) -> Traced | None:
    try:
        fields: tuple[fieldz.Field, ...] = fieldz.fields(obj, parse_annotated=False)
    except TypeError:
        return None
    if ctx.visit(obj):
        return TracedReference.new(obj)

    def field_generator() -> Generator[tuple[str | None, Any]]:
        for field in fields:
            if not field.repr:
                continue
            value: Any = getattr(obj, field.name, fieldz.Field.MISSING)
            if ctx.config.hide_defaults and value is field.default:
                continue
            yield field.name, value

    children: list[TracedItem] = trace_dataclass(ctx, field_generator())
    return TracedContainer(
        children=children,
        cls=type(obj),
        obj_id=id(obj),
        open_brace="(",
        close_brace=")",
    )
