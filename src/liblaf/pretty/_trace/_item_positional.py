from typing import Self, override

import attrs
from rich.text import Text

from liblaf.pretty._lower import LoweredPositionalItem
from liblaf.pretty.literals import EMPTY

from ._context import LowerContext
from ._item_base import TracedItem
from ._node_base import TracedNode
from ._node_leaf import TracedLeaf


@attrs.define
class TracedPositionalItem(TracedItem):
    value: TracedNode

    @classmethod
    def ellipsis(cls, *, prefix: Text = EMPTY, suffix: Text = EMPTY) -> Self:
        return cls(prefix=prefix, value=TracedLeaf.ellipsis(), suffix=suffix)

    def attach(self, value: TracedNode) -> None:
        self.value = value

    @override
    def lower(self, ctx: LowerContext) -> LoweredPositionalItem:
        return LoweredPositionalItem(
            prefix=self.prefix, value=self.value.lower(ctx), suffix=self.suffix
        )
