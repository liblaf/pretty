from __future__ import annotations

import functools

from rich.text import Text

from liblaf.pretty._options import PrettyOptions
from liblaf.pretty._trace._model import (
    Traced,
    TracedContainer,
    TracedDocument,
    TracedField,
    TracedItem,
    TracedKeyValue,
    TracedLeaf,
    TracedReference,
    TracedValue,
)

from ._const import COLON, COMMA, EQUAL
from ._items import Item, ItemKeyValue, ItemValue
from ._model import LowerContext, Lowered, LoweredContainer, LoweredLeaf


def lower(document: TracedDocument, options: PrettyOptions) -> Lowered:
    ctx = LowerContext(
        indent=options.indent,
        obj_id_counts=document.obj_id_counts,
        typenames=document.typenames,
    )
    return _lower_node(document.root, ctx)


@functools.singledispatch
def _lower_node(node: Traced, _ctx: LowerContext) -> Lowered:
    msg = f"unsupported traced node: {type(node)!r}"
    raise TypeError(msg)


@_lower_node.register
def _lower_reference(node: TracedReference, ctx: LowerContext) -> Lowered:
    return LoweredLeaf(value=ctx.make_ref_text(node.cls, node.obj_id))


@_lower_node.register
def _lower_leaf(node: TracedLeaf, ctx: LowerContext) -> Lowered:
    lowered = LoweredLeaf(value=node.text)
    return _annotate(node, lowered, ctx)


@_lower_node.register
def _lower_container(node: TracedContainer, ctx: LowerContext) -> Lowered:
    if not node.items:
        lowered = LoweredLeaf(value=node.empty)
    else:
        lowered = LoweredContainer(
            begin=node.begin,
            end=node.end,
            items=_lower_items(
                node.items, ctx, force_comma_if_single=node.force_comma_if_single
            ),
            indent=ctx.indent,
        )
    return _annotate(node, lowered, ctx)


def _annotate(node: Traced, lowered: Lowered, ctx: LowerContext) -> Lowered:
    if node.obj_id is not None and ctx.obj_id_counts[node.obj_id] > 1:
        lowered.annotation = Text.assemble(
            "  # ", ctx.make_ref_text(node.cls, node.obj_id).plain, style="dim"
        )
    return lowered


def _lower_items(
    items: list[TracedItem], ctx: LowerContext, *, force_comma_if_single: bool
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


@functools.singledispatch
def _lower_item(item: object, _ctx: LowerContext) -> Item:
    msg = f"unsupported traced item: {item!r}"
    raise TypeError(msg)


@_lower_item.register
def _lower_value_item(item: TracedValue, ctx: LowerContext) -> Item:
    if item.value is None:
        msg = "unresolved traced value"
        raise RuntimeError(msg)
    return ItemValue(value=_lower_node(item.value, ctx))


@_lower_item.register
def _lower_field_item(item: TracedField, ctx: LowerContext) -> Item:
    if item.value is None:
        msg = "unresolved traced field"
        raise RuntimeError(msg)
    return ItemKeyValue(
        key=LoweredLeaf(value=Text(item.name, "repr.attrib_name")),
        value=_lower_node(item.value, ctx),
        sep=EQUAL,
    )


@_lower_item.register
def _lower_key_value_item(item: TracedKeyValue, ctx: LowerContext) -> Item:
    if item.key is None or item.value is None:
        msg = "unresolved traced key/value"
        raise RuntimeError(msg)
    return ItemKeyValue(
        key=_lower_node(item.key, ctx),
        value=_lower_node(item.value, ctx),
        sep=COLON,
    )
