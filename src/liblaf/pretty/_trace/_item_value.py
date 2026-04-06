from typing import override

import attrs

from liblaf.pretty._lower import LoweredItemValue

from ._context import LowerContext
from ._item import TracedItem
from ._object import TracedObject
from ._ref import TracedRef


@attrs.define
class TracedItemValue(TracedItem):
    value: TracedObject | TracedRef

    @override
    def lower(self, ctx: LowerContext) -> LoweredItemValue:
        return LoweredItemValue(
            prefix=self.prefix, value=self.value.lower(ctx), suffix=self.suffix
        )

    def attach(self, traced: TracedObject | TracedRef) -> None:
        self.value = traced
