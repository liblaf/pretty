from collections.abc import Callable
from typing import cast

from liblaf.pretty._prelude import PrettyBuilder, PrettySpec, SupportsPretty
from liblaf.pretty._trace._registry import PrettyRegistry
from liblaf.pretty._trace._repr import trace_repr

from ._nodes import TracedNode


def describe(
    obj: object, *, builder: PrettyBuilder, registry: PrettyRegistry
) -> PrettySpec:
    if isinstance(obj, SupportsPretty):
        pretty = cast("Callable[[PrettyBuilder], PrettySpec | None]", obj.__liblaf_pretty__)
        result = pretty(builder)
        if result is not None:
            return result
    handler = registry.resolve(obj)
    if handler is not None:
        result = handler(obj, builder)
        if result is not None:
            return result
    return trace_repr(obj, builder)


def make_node(obj: object, spec: PrettySpec) -> TracedNode:
    return spec.make_node(obj_id=id(obj), cls=type(obj))
