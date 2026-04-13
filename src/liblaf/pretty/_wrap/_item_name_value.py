from __future__ import annotations

from typing import TYPE_CHECKING, override

import attrs
from rich.text import Text

from liblaf.pretty._trace import TRACED_MISSING, TracedNameValueItem
from liblaf.pretty.literals import EQUAL

from ._base import Child
from ._item_base import WrappedItem
from ._node_base import WrappedNode

if TYPE_CHECKING:
    from ._context import TraceContext


@attrs.define
class WrappedNameValueItem(WrappedItem):
    name: Text
    sep: Text = attrs.field(default=EQUAL, kw_only=True)
    value: WrappedNode

    @override
    def trace(self, ctx: TraceContext) -> tuple[tuple[Child], TracedNameValueItem]:
        traced: TracedNameValueItem = TracedNameValueItem(
            prefix=self.prefix,
            name=self.name,
            sep=self.sep,
            value=TRACED_MISSING,
            suffix=self.suffix,
        )
        child: Child = Child(
            wrapped=self.value,
            depth=ctx.depth,
            attach=traced.attach_value,  # ty:ignore[invalid-argument-type]
        )
        return (child,), traced
