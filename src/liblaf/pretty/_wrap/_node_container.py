from __future__ import annotations

from collections.abc import Generator, Iterable
from typing import TYPE_CHECKING, override

import attrs
from rich.text import Text

from liblaf.pretty._trace import TracedContainer, TracedNode

from ._base import Child
from ._item_base import WrappedItem
from ._node_object import WrappedObject

if TYPE_CHECKING:
    from ._context import TraceContext


@attrs.define
class WrappedContainer(WrappedObject):
    begin: Text
    children: Iterable[WrappedItem]
    end: Text
    indent: Text

    def _default_empty(self) -> Text:
        return self.begin + self.end

    empty: Text = attrs.field(
        default=attrs.Factory(_default_empty, takes_self=True), kw_only=True
    )

    def iter_children(
        self, ctx: TraceContext, traced: TracedContainer
    ) -> Generator[Child]:
        for child in self.children:
            yield Child(
                wrapped=child,
                depth=ctx.depth + 1,
                attach=traced.children.append,  # ty:ignore[invalid-argument-type]
            )

    @override
    def trace(self, ctx: TraceContext) -> tuple[Iterable[Child], TracedNode]:
        if (ref := self.visit(ctx)) is not None:
            return (), ref
        traced = TracedContainer(
            begin=self.begin,
            children=[],
            end=self.end,
            indent=self.indent,
            has_ref=False,
            empty=self.empty,
            identifier=self.identifier,
        )
        return self.iter_children(ctx, traced), traced
