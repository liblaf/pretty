from collections.abc import Iterable
from typing import Any

from liblaf.pretty._lower import TracedItem

from ._base import TraceContext
from ._const import ELLIPSIS
from ._registry import trace


def trace_dataclass(
    ctx: TraceContext, fields: Iterable[tuple[str | None, Any]]
) -> list[TracedItem]:
    if ctx.level >= ctx.config.max_level:
        return [ELLIPSIS]
    children: list[TracedItem] = []
    with ctx:
        for name, value in fields:
            if name:
                children.append((name, trace(value, ctx)))
            else:
                children.append(trace(value, ctx))
    return children


def trace_mapping(
    ctx: TraceContext, mapping: Iterable[tuple[Any, Any]]
) -> list[TracedItem]:
    if ctx.level >= ctx.config.max_level:
        return [ELLIPSIS]
    children: list[TracedItem] = []
    with ctx:
        for i, (key, value) in enumerate(mapping):
            if i >= ctx.config.max_dict:
                children.append(ELLIPSIS)
                break
            children.append((trace(key, ctx), trace(value, ctx)))
    return children


def trace_sequence(ctx: TraceContext, sequence: Iterable[Any]) -> list[TracedItem]:
    if ctx.level >= ctx.config.max_level:
        return [ELLIPSIS]
    children: list[TracedItem] = []
    with ctx:
        for i, item in enumerate(sequence):
            if i >= ctx.config.max_list:
                children.append(ELLIPSIS)
                break
            children.append(trace(item, ctx))
    return children
