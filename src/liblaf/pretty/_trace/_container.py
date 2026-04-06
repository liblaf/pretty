from typing import override

import attrs
from rich.text import Text

from liblaf.pretty._lower import LoweredContainer

from ._context import LowerContext
from ._item import TracedItem
from ._object import TracedObject


@attrs.define
class TracedContainer(TracedObject):
    begin: Text
    items: list[TracedItem]
    end: Text
    indent: Text

    @override
    def lower(self, ctx: LowerContext) -> LoweredContainer:
        annotation: Text = self.make_annotation(ctx)
        lowered = LoweredContainer(
            begin=self.begin,
            items=[item.lower(ctx) for item in self.items],
            end=self.end,
            indent=self.indent,
            annotation=annotation,
        )
        return lowered
