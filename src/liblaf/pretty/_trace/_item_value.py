from typing import Self, override

import attrs

from liblaf.pretty._lower import LoweredItemValue

from ._context import LowerContext
from ._item import TracedItem
from ._leaf import TracedLeaf
from ._object import TracedObject
from ._ref import TracedRef


@attrs.define
class TracedItemValue(TracedItem):
    value: TracedObject | TracedRef

    @classmethod
    def ellipsis(cls) -> Self:
        return cls(TracedLeaf.ellipsis())

    @override
    def lower(self, ctx: LowerContext) -> LoweredItemValue:
        return LoweredItemValue(
            prefix=self.prefix, value=self.value.lower(ctx), suffix=self.suffix
        )

    def attach(self, traced: TracedObject | TracedRef) -> None:
        self.value = traced
