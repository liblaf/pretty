from typing import override

import attrs
from rich.text import Text

from liblaf.pretty._const import COMMA
from liblaf.pretty._trace import TracedItemEntry

from ._context import TraceContext
from ._item import SpecItem
from ._spec import Spec
from ._utils import MISSING


@attrs.define
class SpecItemEntry(SpecItem[TracedItemEntry]):
    key: Spec
    value: Spec
    sep: Text = COMMA

    @override
    def trace(self, ctx: TraceContext, depth: int) -> TracedItemEntry:
        traced: TracedItemEntry = TracedItemEntry(
            prefix=self.prefix,
            key=MISSING,
            sep=self.sep,
            value=MISSING,
            suffix=self.suffix,
        )
        ctx.enqueue(self.key, depth, traced.attach_key)
        ctx.enqueue(self.value, depth, traced.attach_value)
        return traced
