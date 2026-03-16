import types

from liblaf.pretty._lower import Traced

from ._base import TraceContext
from ._const import ELLIPSIS, FALSE, NONE, TRUE
from ._registry import trace


@trace.register(bool)
def _trace_bool(obj: bool, _ctx: TraceContext) -> Traced:  # noqa: FBT001
    return TRUE if obj else FALSE


@trace.register(types.EllipsisType)
def _trace_ellipsis(_obj: types.EllipsisType, _ctx: TraceContext) -> Traced:
    return ELLIPSIS


@trace.register(types.NoneType)
def _trace_none(_obj: None, _ctx: TraceContext) -> Traced:
    return NONE


@trace.register(int)
@trace.register(float)
@trace.register(complex)
@trace.register(range)
@trace.register(str)
@trace.register(bytes)
@trace.register(bytearray)
@trace.register(memoryview)
@trace.register(type)
def _trace_scalar(obj: str, ctx: TraceContext) -> Traced:
    return ctx.repr(obj)
