from __future__ import annotations

from typing import TYPE_CHECKING, override

import attrs

from liblaf.pretty._trace import TRACED_MISSING, TracedPositionalItem

from ._base import Child
from ._item_base import WrappedItem
from ._node_base import WrappedNode

if TYPE_CHECKING:
    from ._context import TraceContext


@attrs.define
class WrappedPositionalItem(WrappedItem):
    value: WrappedNode

    @override
    def trace(self, ctx: TraceContext) -> tuple[tuple[Child], TracedPositionalItem]:
        traced: TracedPositionalItem = TracedPositionalItem(
            prefix=self.prefix, value=TRACED_MISSING, suffix=self.suffix
        )
        child: Child = Child(wrapped=self.value, depth=ctx.depth, attach=traced.attach)  # ty:ignore[invalid-argument-type]
        return (child,), traced
