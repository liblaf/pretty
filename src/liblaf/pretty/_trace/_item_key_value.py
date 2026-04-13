from typing import override

import attrs
from rich.text import Text

from liblaf.pretty._lower import LoweredKeyValueItem
from liblaf.pretty.literals import COLON

from ._context import LowerContext
from ._item_base import TracedItem
from ._node_base import TracedNode


@attrs.define
class TracedKeyValueItem(TracedItem):
    key: TracedNode
    sep: Text = attrs.field(default=COLON, kw_only=True)
    value: TracedNode

    def attach_key(self, key: TracedNode) -> None:
        self.key = key

    def attach_value(self, value: TracedNode) -> None:
        self.value = value

    @override
    def lower(self, ctx: LowerContext) -> LoweredKeyValueItem:
        return LoweredKeyValueItem(
            prefix=self.prefix,
            key=self.key.lower(ctx),
            sep=self.sep,
            value=self.value.lower(ctx),
            suffix=self.suffix,
        )
