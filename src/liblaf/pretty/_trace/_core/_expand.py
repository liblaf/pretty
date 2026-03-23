from collections.abc import Callable

from ..._prelude import EntryItemSpec, FieldItemSpec, LiteralSpec, PrettyBuilder, ValueItemSpec
from ._models import (
    TracedChild,
    TracedContainerNode,
    TracedEntryItem,
    TracedFieldItem,
    TracedItem,
    TracedLiteral,
    TracedOccurrence,
    TracedValueItem,
)


def expand_occurrence(
    occurrence: TracedOccurrence,
    *,
    builder: PrettyBuilder,
    discover: Callable[[object, int, tuple[int, ...], tuple[int, ...]], TracedOccurrence],
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
        match item_spec:
            case ValueItemSpec(child=child):
                traced_child, slot_index = trace_child(
                    child,
                    depth=child_depth,
                    path_prefix=occurrence.path,
                    slot_index=slot_index,
                    ancestors=ancestors,
                    discover=discover,
                )
                traced_items.append(
                    TracedValueItem(
                        traced_child,
                        prefix_break=prefix_break,
                        trailing_comma=trailing_comma,
                    )
                )
            case EntryItemSpec(key=key, value=value):
                traced_key, slot_index = trace_child(
                    key,
                    depth=child_depth,
                    path_prefix=occurrence.path,
                    slot_index=slot_index,
                    ancestors=ancestors,
                    discover=discover,
                )
                traced_value, slot_index = trace_child(
                    value,
                    depth=child_depth,
                    path_prefix=occurrence.path,
                    slot_index=slot_index,
                    ancestors=ancestors,
                    discover=discover,
                )
                traced_items.append(
                    TracedEntryItem(
                        traced_key,
                        traced_value,
                        prefix_break=prefix_break,
                        trailing_comma=trailing_comma,
                    )
                )
            case FieldItemSpec(name=name, value=value):
                traced_value, slot_index = trace_child(
                    value,
                    depth=child_depth,
                    path_prefix=occurrence.path,
                    slot_index=slot_index,
                    ancestors=ancestors,
                    discover=discover,
                )
                traced_items.append(
                    TracedFieldItem(
                        name=name,
                        value=traced_value,
                        prefix_break=prefix_break,
                        trailing_comma=trailing_comma,
                    )
                )
            case _:
                raise TypeError(item_spec)
    node.items = tuple(traced_items)
    node.expanded = True


def trace_child(
    child: object,
    *,
    depth: int,
    path_prefix: tuple[int, ...],
    slot_index: int,
    ancestors: tuple[int, ...],
    discover: Callable[[object, int, tuple[int, ...], tuple[int, ...]], TracedOccurrence],
) -> tuple[TracedChild, int]:
    child_path: tuple[int, ...] = (*path_prefix, slot_index)
    match child:
        case LiteralSpec(value=value):
            return TracedLiteral(value), slot_index + 1
        case ValueItemSpec() | EntryItemSpec() | FieldItemSpec():
            raise TypeError("only LiteralSpec may be used as a container child")
        case _:
            return discover(child, depth, child_path, ancestors), slot_index + 1


def truncate_container(
    node: TracedContainerNode, *, builder: PrettyBuilder
) -> tuple[TracedItem, ...]:
    if not node.source_items:
        return ()
    return (TracedValueItem(TracedLiteral(builder.ellipsis().value)),)
