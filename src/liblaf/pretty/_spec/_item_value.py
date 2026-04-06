from typing import override

import attrs

from liblaf.pretty._trace import TracedItemValue

from ._context import TraceContext
from ._item import SpecItem
from ._spec import Spec


@attrs.define
class SpecItemValue(SpecItem):
    value: Spec

    @override
    def trace(self, ctx: TraceContext) -> TracedItemValue:
        return TracedItemValue(
            prefix=self.prefix, value=self.value.trace(ctx), suffix=self.suffix
        )
