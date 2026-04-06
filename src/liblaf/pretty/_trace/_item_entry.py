from typing import override

import attrs
from rich.text import Text

from liblaf.pretty._lower import LoweredItemEntry

from ._context import LowerContext
from ._item import TracedItem
from ._object import TracedObject
from ._ref import TracedRef


@attrs.define
class TracedItemEntry(TracedItem):
    key: TracedObject | TracedRef
    sep: Text
    value: TracedObject | TracedRef

    @override
    def lower(self, ctx: LowerContext) -> LoweredItemEntry:
        return LoweredItemEntry(
            prefix=self.prefix,
            key=self.key.lower(ctx),
            sep=self.sep,
            value=self.value.lower(ctx),
            suffix=self.suffix,
        )

    def attach_key(self, traced: TracedObject | TracedRef) -> None:
        self.key = traced

    def attach_value(self, traced: TracedObject | TracedRef) -> None:
        self.value = traced
