from typing import override

import attrs

from liblaf.pretty._lower import LoweredItemValue

from ._context import LowerContext
from ._item import TracedItem
from ._traced import Traced


@attrs.frozen
class TracedItemValue(TracedItem):
    value: Traced

    @override
    def lower(self, ctx: LowerContext) -> LoweredItemValue:
        return LoweredItemValue(
            prefix=self.prefix, value=self.value.lower(ctx), suffix=self.suffix
        )
