from typing import override

import attrs
from rich.text import Text

from liblaf.pretty._lower import LoweredItemEntry, LoweredLeaf

from ._context import LowerContext
from ._item import TracedItem
from ._object import TracedObject
from ._ref import TracedRef


@attrs.define
class TracedItemField(TracedItem):
    name: Text
    sep: Text
    value: TracedObject | TracedRef

    @override
    def lower(self, ctx: LowerContext) -> LoweredItemEntry:
        return LoweredItemEntry(
            prefix=self.prefix,
            key=LoweredLeaf(self.name),
            sep=self.sep,
            value=self.value.lower(ctx),
            suffix=self.suffix,
        )
