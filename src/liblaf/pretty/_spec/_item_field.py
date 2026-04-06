from typing import override

import attrs
from rich.text import Text

from liblaf.pretty._const import EQUAL
from liblaf.pretty._trace import TracedItemField

from ._context import TraceContext
from ._item import SpecItem
from ._spec import Spec


@attrs.define
class SpecItemField(SpecItem):
    name: Text
    value: Spec
    sep: Text = EQUAL

    @override
    def trace(self, ctx: TraceContext) -> TracedItemField:
        return TracedItemField(
            prefix=self.prefix,
            name=self.name,
            sep=self.sep,
            value=self.value.trace(ctx),
            suffix=self.suffix,
        )
