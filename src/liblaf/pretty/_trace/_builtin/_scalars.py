import types

from liblaf.pretty._prelude import LiteralSpec, PrettyBuilder

from ._const import ELLIPSIS, FALSE, NONE, TRUE
from .._registry import registry
from .._repr import repr_text


@registry.register(bool)
def _trace_bool(obj: bool, _builder: PrettyBuilder) -> LiteralSpec:  # noqa: FBT001
    return TRUE if obj else FALSE


@registry.register(types.EllipsisType)
def _trace_ellipsis(
    _obj: types.EllipsisType, _builder: PrettyBuilder
) -> LiteralSpec:
    return ELLIPSIS


@registry.register(types.NoneType)
def _trace_none(_obj: None, _builder: PrettyBuilder) -> LiteralSpec:
    return NONE


@registry.register(int)
@registry.register(float)
@registry.register(complex)
@registry.register(range)
@registry.register(str)
@registry.register(bytes)
@registry.register(bytearray)
@registry.register(memoryview)
@registry.register(type)
def _trace_scalar(obj: object, builder: PrettyBuilder) -> LiteralSpec:
    return LiteralSpec(repr_text(obj, builder))
