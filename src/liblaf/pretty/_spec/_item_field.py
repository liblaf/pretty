from typing import override

import attrs
from rich.text import Text

from liblaf.pretty._const import EQUAL
from liblaf.pretty._trace import TracedItemField

from ._context import TraceContext
from ._item import SpecItem
from ._spec import Spec
from ._utils import MISSING


@attrs.define
class SpecItemField(SpecItem[TracedItemField]):
    name: Text
    value: Spec
    sep: Text = EQUAL

    @override
    def trace(self, ctx: TraceContext, depth: int) -> TracedItemField:
        traced: TracedItemField = TracedItemField(
            prefix=self.prefix,
            name=self.name,
            sep=self.sep,
            value=MISSING,
            suffix=self.suffix,
        )
        ctx.enqueue(self.value, depth, traced.attach)
        return traced
