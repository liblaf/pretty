from __future__ import annotations

from collections import Counter
from typing import Protocol

from rich.text import Text

from liblaf.pretty._options import PrettyOptions

from ._const import COMMA
from ._items import Item
from ._model import LowerContext, Lowered


class LowerableNode(Protocol):
    cls: type
    obj_id: int | None

    def lower(self, ctx: LowerContext) -> Lowered: ...


class LowerableItem(Protocol):
    def lower(self, ctx: LowerContext) -> Item: ...


class LowerableDocument(Protocol):
    root: LowerableNode
    obj_id_counts: Counter[int]
    typenames: dict[type, str]


def lower(document: LowerableDocument, options: PrettyOptions) -> Lowered:
    ctx = LowerContext(
        indent=options.indent,
        obj_id_counts=document.obj_id_counts,
        typenames=document.typenames,
    )
    return _lower_node(document.root, ctx)


def _lower_node(node: LowerableNode, ctx: LowerContext) -> Lowered:
    return node.lower(ctx)


def _annotate(node: LowerableNode, lowered: Lowered, ctx: LowerContext) -> Lowered:
    if node.obj_id is not None and ctx.obj_id_counts[node.obj_id] > 1:
        lowered.annotation = Text.assemble(
            "  # ", ctx.make_ref_text(node.cls, node.obj_id).plain, style="dim"
        )
    return lowered


def _lower_items(
    items: list[LowerableItem], ctx: LowerContext, *, force_comma_if_single: bool
) -> list[Item]:
    lowered_items: list[Item] = [_lower_item(item, ctx) for item in items]
    for index, item in enumerate(lowered_items):
        if index > 0:
            item.prefix = Text(" ")
        if index < len(lowered_items) - 1 or (
            force_comma_if_single and len(lowered_items) == 1
        ):
            item.suffix = COMMA.copy()
    return lowered_items


def _lower_item(item: LowerableItem, ctx: LowerContext) -> Item:
    return item.lower(ctx)
