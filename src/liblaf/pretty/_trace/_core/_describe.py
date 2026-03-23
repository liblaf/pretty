from ..._prelude import ContainerSpec, LeafSpec, LiteralSpec, PrettyBuilder, PrettySpec
from .._registry import PrettyRegistry
from .._repr import trace_repr
from ._models import TracedContainerNode, TracedLeafNode, TracedNode


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
    obj_id: int = id(obj)
    cls: type = type(obj)
    match spec:
        case LiteralSpec(value=value):
            return TracedLeafNode(obj_id=obj_id, cls=cls, referable=False, value=value)
        case LeafSpec(value=value, referable=referable):
            return TracedLeafNode(
                obj_id=obj_id, cls=cls, referable=referable, value=value
            )
        case ContainerSpec() as container:
            return TracedContainerNode(
                obj_id=obj_id,
                cls=cls,
                referable=container.referable,
                open_brace=container.open_brace,
                close_brace=container.close_brace,
                empty_open_brace=container.empty_open_brace,
                empty_close_brace=container.empty_close_brace,
                show_type_name=container.show_type_name,
                trailing_comma_single=container.trailing_comma_single,
                source_items=container.items,
            )
        case _:
            raise TypeError(spec)
