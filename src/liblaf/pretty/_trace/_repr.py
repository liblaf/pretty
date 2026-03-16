from liblaf.pretty._lower import Traced, TracedReference

from ._base import TraceContext


def trace_repr(obj: object, ctx: TraceContext) -> Traced:
    if ctx.visit(obj):
        return TracedReference.new(obj)
    return ctx.repr(obj)
