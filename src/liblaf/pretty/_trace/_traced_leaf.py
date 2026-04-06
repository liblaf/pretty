from typing import override

import attrs
from rich.text import Text

from liblaf.pretty._const import EMPTY
from liblaf.pretty._lower import LoweredLeaf

from ._context import LowerContext
from ._traced import Traced


@attrs.frozen
class TracedLeaf(Traced):
    value: Text
    anchor: bool = False

    @override
    def lower(self, ctx: LowerContext) -> LoweredLeaf:
        annotation: Text = ctx.make_anchor(self.cls, self.id_) if self.anchor else EMPTY
        return LoweredLeaf(self.value, annotation=annotation)
