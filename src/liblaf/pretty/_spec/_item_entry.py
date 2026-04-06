from typing import override

import attrs
from rich.text import Text

from liblaf.pretty._const import COMMA
from liblaf.pretty._trace import TracedItemEntry

from ._context import TraceContext
from ._item import SpecItem
from ._spec import Spec


@attrs.define
class SpecItemEntry(SpecItem):
    key: Spec
    value: Spec
    sep: Text = COMMA

    @override
    def trace(self, ctx: TraceContext) -> TracedItemEntry:
        return TracedItemEntry(
            prefix=self.prefix,
            key=self.key.trace(ctx),
            sep=self.sep,
            value=self.value.trace(ctx),
            suffix=self.suffix,
        )
