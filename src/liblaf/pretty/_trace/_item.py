from __future__ import annotations

from typing import TYPE_CHECKING, override

import attrs
from rich.text import Text

from liblaf.pretty._const import COLON, EMPTY, EQUAL
from liblaf.pretty._lower import (
    LoweredEntryItem,
    LoweredItem,
    LoweredLeaf,
    LoweredValueItem,
)

from ._base import Traced
from ._context import LowerContext
from ._sentinel import TRUNCATED

if TYPE_CHECKING:
    from ._node import TracedNode


@attrs.define
class TracedDictItem(Traced):
    prefix: Text = attrs.field(default=EMPTY, kw_only=True)
    key: TracedNode
    sep: Text = attrs.field(default=COLON, kw_only=True)
    value: TracedNode
    suffix: Text = attrs.field(default=EMPTY, kw_only=True)

    @override
    def lower(self, ctx: LowerContext) -> LoweredItem:
        if self.key is TRUNCATED or self.value is TRUNCATED:
            return LoweredValueItem.ellipsis(prefix=self.prefix, suffix=self.suffix)
        return LoweredEntryItem(
            prefix=self.prefix,
            key=self.key.lower(ctx),
            sep=self.sep,
            value=self.value.lower(ctx),
            suffix=self.suffix,
        )

    def attach_key(self, traced: TracedNode) -> None:
        self.key = traced

    def attach_value(self, traced: TracedNode) -> None:
        self.value = traced


@attrs.define
class TracedNamedItem(Traced):
    prefix: Text = attrs.field(default=EMPTY, kw_only=True)
    name: Text
    sep: Text = attrs.field(default=EQUAL, kw_only=True)
    value: TracedNode
    suffix: Text = attrs.field(default=EMPTY, kw_only=True)

    @override
    def lower(self, ctx: LowerContext) -> LoweredItem:
        if self.value is TRUNCATED:
            return LoweredValueItem.ellipsis(prefix=self.prefix, suffix=self.suffix)
        return LoweredEntryItem(
            prefix=self.prefix,
            key=LoweredLeaf(self.name),
            sep=self.sep,
            value=self.value.lower(ctx),
            suffix=self.suffix,
        )

    def attach_value(self, traced: TracedNode) -> None:
        self.value = traced


@attrs.define
class TracedValueItem(Traced):
    prefix: Text = attrs.field(default=EMPTY, kw_only=True)
    value: TracedNode
    suffix: Text = attrs.field(default=EMPTY, kw_only=True)

    @classmethod
    def ellipsis(cls, prefix: Text = EMPTY, suffix: Text = EMPTY) -> TracedValueItem:
        from ._node import TracedLeaf

        return cls(prefix=prefix, value=TracedLeaf.ellipsis(), suffix=suffix)

    @override
    def lower(self, ctx: LowerContext) -> LoweredValueItem:
        if self.value is TRUNCATED:
            return LoweredValueItem.ellipsis(prefix=self.prefix, suffix=self.suffix)
        return LoweredValueItem(
            prefix=self.prefix, value=self.value.lower(ctx), suffix=self.suffix
        )

    def attach(self, traced: TracedNode) -> None:
        self.value = traced


type TracedItem = TracedDictItem | TracedNamedItem | TracedValueItem
