from typing import override

import attrs

from liblaf.pretty._trace import TracedItemValue

from ._context import TraceContext
from ._item import SpecItem
from ._spec import Spec
from ._utils import MISSING


@attrs.define
class SpecItemValue(SpecItem):
    value: Spec

    @override
    def trace(self, ctx: TraceContext, depth: int) -> TracedItemValue:
        traced: TracedItemValue = TracedItemValue(
            prefix=self.prefix, value=MISSING, suffix=self.suffix
        )
        ctx.enqueue(self.value, depth, traced.attach)
        return traced
