from __future__ import annotations

from typing import TYPE_CHECKING, override

import attrs
from rich.text import Text

from liblaf.pretty._const import COLON, EMPTY, EQUAL
from liblaf.pretty._lower import LoweredItemEntry, LoweredItemValue, LoweredLeaf

from ._base import Traced
from ._context import LowerContext

if TYPE_CHECKING:
    from ._node import TracedNode


@attrs.define
class TracedEntry(Traced):
    prefix: Text = attrs.field(default=EMPTY, kw_only=True)
    key: TracedNode
    sep: Text = attrs.field(default=COLON, kw_only=True)
    value: TracedNode
    suffix: Text = attrs.field(default=EMPTY, kw_only=True)

    @override
    def lower(self, ctx: LowerContext) -> LoweredItemEntry:
        return LoweredItemEntry(
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
class TracedField(Traced):
    prefix: Text = attrs.field(default=EMPTY, kw_only=True)
    name: Text
    sep: Text = attrs.field(default=EQUAL, kw_only=True)
    value: TracedNode
    suffix: Text = attrs.field(default=EMPTY, kw_only=True)

    @override
    def lower(self, ctx: LowerContext) -> LoweredItemEntry:
        return LoweredItemEntry(
            prefix=self.prefix,
            key=LoweredLeaf(self.name),
            sep=self.sep,
            value=self.value.lower(ctx),
            suffix=self.suffix,
        )

    def attach_value(self, traced: TracedNode) -> None:
        self.value = traced


@attrs.define
class TracedElem(Traced):
    prefix: Text = attrs.field(default=EMPTY, kw_only=True)
    value: TracedNode
    suffix: Text = attrs.field(default=EMPTY, kw_only=True)

    @override
    def lower(self, ctx: LowerContext) -> LoweredItemValue:
        return LoweredItemValue(
            prefix=self.prefix, value=self.value.lower(ctx), suffix=self.suffix
        )

    def attach(self, traced: TracedNode) -> None:
        self.value = traced


type TracedItem = TracedEntry | TracedField | TracedElem
