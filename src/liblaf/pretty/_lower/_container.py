from typing import TYPE_CHECKING

from rich.text import Text

from .._compile import BREAK, COLON, COMMA, EMPTY, EQUAL, Item, ItemKeyValue, ItemValue
from .._compile import Lowered, LoweredContainer, LoweredLeaf
from .._trace import (
    TracedContainerNode,
    TracedEntryItem,
    TracedFieldItem,
    TracedLiteral,
    TracedOccurrence,
    TracedValueItem,
)

if TYPE_CHECKING:
    from ._lowerer import Lowerer


def lower_container(
    lowerer: "Lowerer",
    node: TracedContainerNode,
    *,
    inline_repeat: bool,
    ancestors: tuple[int, ...],
) -> Lowered:
    if not node.items:
        return LoweredLeaf(
            Text.assemble(
                *type_name_segment(lowerer, node),
                (node.empty_open_brace, "repr.tag_start"),
                (node.empty_close_brace, "repr.tag_end"),
            )
        )
    child_ancestors: tuple[int, ...] = (*ancestors, node.obj_id)
    items: list[Item] = []
    for item in node.items:
        prefix: Text = BREAK if item.prefix_break else EMPTY
        suffix: Text = COMMA if item.trailing_comma else EMPTY
        match item:
            case TracedValueItem(child=child):
                items.append(
                    ItemValue(
                        lower_child(lowerer, child, inline_repeat, child_ancestors),
                        prefix=prefix,
                        suffix=suffix,
                    )
                )
            case TracedEntryItem(key=key, value=value):
                items.append(
                    ItemKeyValue(
                        key=lower_child(lowerer, key, inline_repeat, child_ancestors),
                        value=lower_child(
                            lowerer, value, inline_repeat, child_ancestors
                        ),
                        sep=COLON,
                        prefix=prefix,
                        suffix=suffix,
                    )
                )
            case TracedFieldItem(name=name, value=value):
                items.append(
                    ItemKeyValue(
                        key=LoweredLeaf(Text(name, "repr.attrib_name")),
                        value=lower_child(
                            lowerer, value, inline_repeat, child_ancestors
                        ),
                        sep=EQUAL,
                        prefix=prefix,
                        suffix=suffix,
                    )
                )
            case _:
                raise TypeError(item)
    begin: Text = Text.assemble(
        *type_name_segment(lowerer, node), (node.open_brace, "repr.tag_start")
    )
    end: Text = Text(node.close_brace, "repr.tag_end")
    return LoweredContainer(begin=begin, end=end, items=items, indent=lowerer.ctx.indent)


def lower_child(
    lowerer: "Lowerer",
    child: TracedLiteral | TracedOccurrence,
    inline_repeat: bool,
    ancestors: tuple[int, ...],
) -> Lowered:
    match child:
        case TracedLiteral(value=value):
            return LoweredLeaf(value.copy())
        case TracedOccurrence():
            return lowerer.lower_occurrence(
                child, inline_repeat=inline_repeat, ancestors=ancestors
            )
        case _:
            raise TypeError(child)


def type_name_segment(
    lowerer: "Lowerer", node: TracedContainerNode
) -> tuple[tuple[str, str], ...]:
    if not node.show_type_name:
        return ()
    return ((lowerer.ctx.typenames[node.cls], "repr.tag_name"),)
