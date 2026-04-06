from typing import override

import attrs
from rich.text import Text

from liblaf.pretty._const import EMPTY
from liblaf.pretty._lower import LoweredContainer

from ._context import LowerContext
from ._item import TracedItem
from ._traced import Traced


@attrs.frozen
class TracedContainer(Traced):
    begin: Text
    end: Text
    items: list[TracedItem]
    indent: Text
    anchor: bool = False

    @override
    def lower(self, ctx: LowerContext) -> LoweredContainer:
        annotation: Text = ctx.make_anchor(self.cls, self.id_) if self.anchor else EMPTY
        lowered = LoweredContainer(
            begin=self.begin,
            end=self.end,
            items=[item.lower(ctx) for item in self.items],
            indent=self.indent,
            annotation=annotation,
        )
        return lowered
