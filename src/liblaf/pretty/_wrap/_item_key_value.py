from __future__ import annotations

from typing import TYPE_CHECKING, override

import attrs
from rich.text import Text

from liblaf.pretty._trace import TRACED_MISSING, TracedKeyValueItem
from liblaf.pretty.literals import COLON

from ._base import Child
from ._item_base import WrappedItem
from ._node_base import WrappedNode

if TYPE_CHECKING:
    from ._context import TraceContext


@attrs.define
class WrappedKeyValueItem(WrappedItem):
    key: WrappedNode
    sep: Text = attrs.field(default=COLON, kw_only=True)
    value: WrappedNode

    @override
    def trace(
        self, ctx: TraceContext
    ) -> tuple[tuple[Child, Child], TracedKeyValueItem]:
        traced: TracedKeyValueItem = TracedKeyValueItem(
            prefix=self.prefix,
            key=TRACED_MISSING,
            sep=self.sep,
            value=TRACED_MISSING,
            suffix=self.suffix,
        )
        key: Child = Child(
            wrapped=self.key,
            depth=ctx.depth,
            attach=traced.attach_key,  # ty:ignore[invalid-argument-type]
        )
        value: Child = Child(
            wrapped=self.value,
            depth=ctx.depth,
            attach=traced.attach_value,  # ty:ignore[invalid-argument-type]
        )
        return (key, value), traced
