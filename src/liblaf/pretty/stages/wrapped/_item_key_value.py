from typing import override

import attrs
from rich.text import Text

from liblaf.pretty.literals import COLON
from liblaf.pretty.stages.traced import TRACED_MISSING, TracedKeyValueItem

from ._base import WrappedChild
from ._context import TraceContext
from ._item_base import WrappedItem
from ._node_base import WrappedNode


@attrs.define
class WrappedKeyValueItem(WrappedItem):
    key: WrappedNode
    sep: Text = attrs.field(default=COLON, kw_only=True)
    value: WrappedNode

    @override
    def trace(
        self, ctx: TraceContext
    ) -> tuple[tuple[WrappedChild, WrappedChild], TracedKeyValueItem]:
        traced: TracedKeyValueItem = TracedKeyValueItem(
            prefix=self.prefix,
            key=TRACED_MISSING,
            sep=self.sep,
            value=TRACED_MISSING,
            suffix=self.suffix,
        )
        key: WrappedChild = WrappedChild(
            wrapped=self.key,
            depth=ctx.depth,
            attach=traced.attach_key,  # ty:ignore[invalid-argument-type]
        )
        value: WrappedChild = WrappedChild(
            wrapped=self.value,
            depth=ctx.depth,
            attach=traced.attach_value,  # ty:ignore[invalid-argument-type]
        )
        return (key, value), traced
