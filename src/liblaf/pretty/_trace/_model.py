from __future__ import annotations

import abc
from collections import Counter
from typing import TYPE_CHECKING, cast

import attrs
from rich.text import Text

if TYPE_CHECKING:
    from liblaf.pretty._lower._api import LowerableItem
    from liblaf.pretty._lower._items import Item
    from liblaf.pretty._lower._model import LowerContext, Lowered


@attrs.define
class TracedDocument:
    root: Traced
    obj_id_counts: Counter[int]
    typenames: dict[type, str]


@attrs.define
class Traced(abc.ABC):
    cls: type
    obj_id: int | None = None

    def lower(self, ctx: LowerContext) -> Lowered:
        del ctx
        msg = f"unsupported traced node: {type(self)!r}"
        raise TypeError(msg)


@attrs.define(kw_only=True)
class TracedLeaf(Traced):
    text: Text = attrs.field(converter=lambda value: value.copy())

    def lower(self, ctx: LowerContext) -> Lowered:
        from liblaf.pretty._lower._api import _annotate
        from liblaf.pretty._lower._model import LoweredLeaf

        lowered = LoweredLeaf(value=self.text)
        return _annotate(self, lowered, ctx)


@attrs.define(kw_only=True)
class TracedReference(Traced):
    obj_id: int

    def lower(self, ctx: LowerContext) -> Lowered:
        from liblaf.pretty._lower._model import LoweredLeaf

        return LoweredLeaf(value=ctx.make_ref_text(self.cls, self.obj_id))


@attrs.define
class TracedItem:
    def lower(self, ctx: LowerContext) -> Item:
        del ctx
        msg = f"unsupported traced item: {self!r}"
        raise TypeError(msg)


@attrs.define
class TracedValue(TracedItem):
    value: Traced | None = None

    def lower(self, ctx: LowerContext) -> Item:
        from liblaf.pretty._lower._api import _lower_node
        from liblaf.pretty._lower._items import ItemValue

        if self.value is None:
            msg = "unresolved traced value"
            raise RuntimeError(msg)
        return ItemValue(value=_lower_node(self.value, ctx))


@attrs.define
class TracedField(TracedItem):
    name: str
    value: Traced | None = None

    def lower(self, ctx: LowerContext) -> Item:
        from liblaf.pretty._lower._api import _lower_node
        from liblaf.pretty._lower._const import EQUAL
        from liblaf.pretty._lower._items import ItemKeyValue
        from liblaf.pretty._lower._model import LoweredLeaf

        if self.value is None:
            msg = "unresolved traced field"
            raise RuntimeError(msg)
        return ItemKeyValue(
            key=LoweredLeaf(value=Text(self.name, "repr.attrib_name")),
            value=_lower_node(self.value, ctx),
            sep=EQUAL,
        )


@attrs.define
class TracedKeyValue(TracedItem):
    key: Traced | None = None
    value: Traced | None = None

    def lower(self, ctx: LowerContext) -> Item:
        from liblaf.pretty._lower._api import _lower_node
        from liblaf.pretty._lower._const import COLON
        from liblaf.pretty._lower._items import ItemKeyValue

        if self.key is None or self.value is None:
            msg = "unresolved traced key/value"
            raise RuntimeError(msg)
        return ItemKeyValue(
            key=_lower_node(self.key, ctx),
            value=_lower_node(self.value, ctx),
            sep=COLON,
        )


@attrs.define(kw_only=True)
class TracedContainer(Traced):
    begin: Text = attrs.field(converter=lambda value: value.copy())
    end: Text = attrs.field(converter=lambda value: value.copy())
    empty: Text = attrs.field(converter=lambda value: value.copy())
    items: list[TracedItem] = attrs.field(factory=list)
    force_comma_if_single: bool = False

    def lower(self, ctx: LowerContext) -> Lowered:
        from liblaf.pretty._lower._api import _annotate, _lower_items
        from liblaf.pretty._lower._model import LoweredContainer, LoweredLeaf

        if not self.items:
            lowered = LoweredLeaf(value=self.empty)
        else:
            lowered = LoweredContainer(
                begin=self.begin,
                end=self.end,
                items=_lower_items(
                    cast("list[LowerableItem]", self.items),
                    ctx,
                    force_comma_if_single=self.force_comma_if_single,
                ),
                indent=ctx.indent,
            )
        return _annotate(self, lowered, ctx)
