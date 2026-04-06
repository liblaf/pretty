from typing import override

import attrs
from rich.text import Text

from liblaf.pretty._const import COMMA
from liblaf.pretty._lower import LoweredItemEntry

from ._context import LowerContext
from ._item import TracedItem
from ._traced import Traced


@attrs.frozen
class TracedItemEntry(TracedItem):
    key: Traced
    value: Traced
    sep: Text = COMMA

    @override
    def lower(self, ctx: LowerContext) -> LoweredItemEntry:
        return LoweredItemEntry(
            prefix=self.prefix,
            key=self.key.lower(ctx),
            sep=self.sep,
            value=self.value.lower(ctx),
            suffix=self.suffix,
        )
