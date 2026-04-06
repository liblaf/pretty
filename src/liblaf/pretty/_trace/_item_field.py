from typing import override

import attrs
from rich.text import Text

from liblaf.pretty._const import EQUAL
from liblaf.pretty._lower import LoweredItemEntry, LoweredLeaf

from ._context import LowerContext
from ._item import TracedItem
from ._traced import Traced


@attrs.frozen
class TracedItemField(TracedItem):
    name: Text
    value: Traced
    sep: Text = EQUAL

    @override
    def lower(self, ctx: LowerContext) -> LoweredItemEntry:
        return LoweredItemEntry(
            prefix=self.prefix,
            key=LoweredLeaf(self.name),
            sep=self.sep,
            value=self.value.lower(ctx),
            suffix=self.suffix,
        )
