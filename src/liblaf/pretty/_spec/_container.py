from collections.abc import Iterable
from typing import override

import attrs
from rich.text import Text

from liblaf.pretty._const import INDENT
from liblaf.pretty._trace import (
    TracedContainer,
    TracedItemValue,
    TracedObject,
    TracedRef,
)

from ._context import TraceContext
from ._item import SpecItem
from ._object import SpecObject


@attrs.define
class SpecContainer(SpecObject[TracedObject | TracedRef]):
    begin: Text
    items: Iterable[SpecItem]
    end: Text

    def _default_empty(self) -> Text:
        return self.begin[0] + self.end[-1]

    empty: Text = attrs.field(
        default=attrs.Factory(_default_empty, takes_self=True), kw_only=True
    )
    indent: Text = attrs.field(default=INDENT, kw_only=True)

    @override
    def trace(self, ctx: TraceContext, depth: int) -> TracedContainer | TracedRef:
        if (traced := self.visited(ctx)) is not None:
            return traced
        traced: TracedContainer = TracedContainer(
            begin=self.begin,
            items=[],
            end=self.end,
            indent=self.indent,
            empty=self.empty,
            ref=self.ref,
        )
        if depth < ctx.options.max_level:
            for item in self.items:
                ctx.enqueue(item, depth + 1, traced.items.append)
        else:
            traced.items = [TracedItemValue.ellipsis()]
        ctx.traced[self.ref.id_] = traced
        return traced
