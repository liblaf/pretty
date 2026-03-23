from collections.abc import Callable

from liblaf.pretty._prelude._helpers._builder import PrettyBuilder
from liblaf.pretty._prelude._helpers._items import ItemSpec
from liblaf.pretty._prelude._helpers._specs import LiteralSpec

from ._items import LowerableChild, TracedItem, TracedValueItem
from ._nodes import TracedContainerNode
from ._occurrence import TracedOccurrence

_ONLY_LITERAL_CHILD = "only LiteralSpec may be used as a container child"


def expand_occurrence(
    occurrence: TracedOccurrence,
    *,
    discover: Callable[
        [object, int, tuple[int, ...], tuple[int, ...]], TracedOccurrence
    ],
) -> None:
    node = occurrence.node
    if not isinstance(node, TracedContainerNode) or node.expanded:
        return
    traced_items: list[TracedItem] = []
    slot_index: int = 0
    child_depth: int = occurrence.depth + 1
    ancestors: tuple[int, ...] = (*occurrence.ancestors, node.obj_id)
    item_count: int = len(node.source_items)
    for item_index, item_spec in enumerate(node.source_items):
        prefix_break: bool = item_index > 0
        trailing_comma: bool = item_index < item_count - 1 or (
            node.trailing_comma_single and item_count == 1
        )
        traced_item, slot_index = item_spec.trace_item(
            prefix_break=prefix_break,
            trailing_comma=trailing_comma,
            slot_index=slot_index,
            trace_child=lambda child, child_slot: trace_child(
                child,
                depth=child_depth,
                path_prefix=occurrence.path,
                slot_index=child_slot,
                ancestors=ancestors,
                discover=discover,
            ),
        )
        traced_items.append(traced_item)
    node.items = tuple(traced_items)
    node.expanded = True


def trace_child(
    child: object,
    *,
    depth: int,
    path_prefix: tuple[int, ...],
    slot_index: int,
    ancestors: tuple[int, ...],
    discover: Callable[
        [object, int, tuple[int, ...], tuple[int, ...]], TracedOccurrence
    ],
) -> tuple[LowerableChild, int]:
    child_path: tuple[int, ...] = (*path_prefix, slot_index)
    if isinstance(child, LiteralSpec):
        return child.trace_child(), slot_index + 1
    if isinstance(child, ItemSpec):
        raise TypeError(_ONLY_LITERAL_CHILD)
    return discover(child, depth, child_path, ancestors), slot_index + 1


def truncate_container(
    node: TracedContainerNode, *, builder: PrettyBuilder
) -> tuple[TracedItem, ...]:
    if not node.source_items:
        return ()
    return (TracedValueItem(builder.ellipsis().trace_child()),)
