from liblaf.pretty._lower import Traced, TracedContainer, TracedItem, TracedReference

from ._base import TraceContext
from ._registry import trace
from ._utils import trace_mapping, trace_sequence


@trace.register(list)
def _trace_list(obj: list, ctx: TraceContext) -> Traced:
    if ctx.visit(obj):
        return TracedReference.new(obj)

    children: list[TracedItem] = trace_sequence(ctx, obj)
    return TracedContainer(
        cls=list, obj_id=id(obj), open_brace="[", close_brace="]", children=children
    )


@trace.register(tuple)
def _trace_tuple(obj: tuple, ctx: TraceContext) -> Traced:
    if ctx.visit(obj):
        return TracedReference.new(obj)
    children: list[TracedItem] = trace_sequence(ctx, obj)
    return TracedContainer(
        cls=tuple,
        obj_id=id(obj),
        open_brace="(",
        close_brace=")",
        children=children,
        force_comma_if_single=True,
    )


@trace.register(set)
def _trace_set(obj: set, ctx: TraceContext) -> Traced:
    if ctx.visit(obj):
        return TracedReference.new(obj)
    children: list[TracedItem] = trace_sequence(ctx, obj)
    return TracedContainer(
        cls=set, obj_id=id(obj), open_brace="{", close_brace="}", children=children
    )


@trace.register(frozenset)
def _trace_frozenset(obj: frozenset, ctx: TraceContext) -> Traced:
    if ctx.visit(obj):
        return TracedReference.new(obj)
    children: list[TracedItem] = trace_sequence(ctx, obj)
    return TracedContainer(
        cls=frozenset,
        obj_id=id(obj),
        open_brace="({",
        close_brace="})",
        children=children,
    )


@trace.register(dict)
def _trace_dict(obj: dict, ctx: TraceContext) -> Traced:
    if ctx.visit(obj):
        return TracedReference.new(obj)
    children: list[TracedItem] = trace_mapping(ctx, obj.items())
    return TracedContainer(
        cls=dict, obj_id=id(obj), open_brace="{", close_brace="}", children=children
    )
