from __future__ import annotations

from typing import TYPE_CHECKING, Self, cast, override

import attrs
from rich.text import Text

from liblaf.pretty._const import COLON, EMPTY, EQUAL
from liblaf.pretty._trace import (
    TracedDictItem,
    TracedNamedItem,
    TracedNode,
    TracedValueItem,
)

from ._base import Spec
from ._context import TraceContext

if TYPE_CHECKING:
    from ._node import SpecNode


_MISSING: TracedNode = cast("TracedNode", None)


@attrs.define
class SpecDictItem(Spec):
    prefix: Text = attrs.field(default=EMPTY, kw_only=True)
    key: SpecNode
    sep: Text = attrs.field(default=COLON, kw_only=True)
    value: SpecNode
    suffix: Text = attrs.field(default=EMPTY, kw_only=True)

    @override
    def trace(self, ctx: TraceContext, depth: int) -> TracedDictItem:
        traced: TracedDictItem = TracedDictItem(
            prefix=self.prefix,
            key=_MISSING,
            sep=self.sep,
            value=_MISSING,
            suffix=self.suffix,
        )
        ctx.enqueue(self.key, depth, traced.attach_key)
        ctx.enqueue(self.value, depth, traced.attach_value)
        return traced


@attrs.define
class SpecNamedItem(Spec):
    prefix: Text = attrs.field(default=EMPTY, kw_only=True)
    name: Text
    sep: Text = attrs.field(default=EQUAL, kw_only=True)
    value: SpecNode
    suffix: Text = attrs.field(default=EMPTY, kw_only=True)

    @override
    def trace(self, ctx: TraceContext, depth: int) -> TracedNamedItem:
        traced: TracedNamedItem = TracedNamedItem(
            prefix=self.prefix,
            name=self.name,
            sep=self.sep,
            value=_MISSING,
            suffix=self.suffix,
        )
        ctx.enqueue(self.value, depth, traced.attach_value)
        return traced


@attrs.define
class SpecValueItem(Spec):
    prefix: Text = attrs.field(default=EMPTY, kw_only=True)
    value: SpecNode
    suffix: Text = attrs.field(default=EMPTY, kw_only=True)

    @classmethod
    def ellipsis(cls) -> Self:
        from ._node import SpecLeaf

        return cls(SpecLeaf.ellipsis())

    @override
    def trace(self, ctx: TraceContext, depth: int) -> TracedValueItem:
        traced: TracedValueItem = TracedValueItem(
            prefix=self.prefix, value=_MISSING, suffix=self.suffix
        )
        ctx.enqueue(self.value, depth, traced.attach)
        return traced


type SpecItem = SpecDictItem | SpecNamedItem | SpecValueItem
