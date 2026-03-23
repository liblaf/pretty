from ..._prelude import PrettyBuilder, PrettySpec
from .._registry import PrettyRegistry
from .._repr import trace_repr
from ._nodes import TracedNode


def describe(
    obj: object, *, builder: PrettyBuilder, registry: PrettyRegistry
) -> PrettySpec:
    if hasattr(obj, "__liblaf_pretty__"):
        result = obj.__liblaf_pretty__(builder)
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
