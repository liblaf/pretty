from typing import override

import attrs
from rich.text import Text

from liblaf.pretty._lower import LoweredContainer, LoweredLeaf

from ._context import LowerContext
from ._item import TracedItem
from ._object import TracedObject


@attrs.define
class TracedContainer(TracedObject):
    begin: Text
    items: list[TracedItem]
    end: Text
    indent: Text

    def _default_empty(self) -> Text:
        return self.begin + self.end

    empty: Text = attrs.field(
        default=attrs.Factory(_default_empty, takes_self=True), kw_only=True
    )

    @override
    def lower(self, ctx: LowerContext) -> LoweredContainer | LoweredLeaf:
        annotation: Text = self.make_annotation(ctx)
        typename: str = ctx.get_tag_typename(self.ref.cls)
        if not self.items:
            return LoweredLeaf(
                Text.assemble((typename, "repr.tag_name"), self.empty),
                annotation=annotation,
            )
        lowered = LoweredContainer(
            begin=Text.assemble((typename, "repr.tag_name"), self.begin),
            items=[item.lower(ctx) for item in self.items],
            end=self.end,
            indent=self.indent,
            annotation=annotation,
        )
        return lowered

    def append(self, traced: TracedItem) -> None:
        self.items.append(traced)
