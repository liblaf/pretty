from typing import override

import attrs
from rich.text import Text

from liblaf.pretty.literals import ELLIPSIS, EMPTY
from liblaf.pretty.stages.lower import Lowered, LoweredContainer, LoweredLeaf

from ._base import Traced
from ._context import LowerContext
from ._identifier import Identifier
from ._item import TracedItems


@attrs.define
class TracedContainer(Traced):
    begin: Text
    doc: TracedItems
    end: Text
    indent: Text = attrs.field(kw_only=True)
    has_ref: bool = attrs.field(default=False, kw_only=True)
    identifier: Identifier = attrs.field(kw_only=True)

    def _default_empty(self) -> Text:
        return Text.assemble(self.begin, self.end)

    empty: Text = attrs.field(
        default=attrs.Factory(_default_empty, takes_self=True), kw_only=True
    )

    @override
    def lower(self, ctx: LowerContext) -> Lowered:
        comment: Text = ctx.make_comment(self.identifier) if self.has_ref else EMPTY
        typename: str = ctx.get_tag_typename(self.identifier.cls)
        if self.doc.empty:
            return LoweredLeaf(
                Text.assemble((typename, "repr.tag_name"), self.empty), comment=comment
            )
        begin: Text = Text.assemble((typename, "repr.tag_name"), self.begin)
        if self.doc.truncated:
            return LoweredLeaf(
                Text.assemble(begin, ELLIPSIS, self.end), comment=comment
            )
        return LoweredContainer(
            begin=begin,
            doc=self.doc.lower(ctx),
            end=self.end,
            indent=self.indent,
            comment=comment,
        )
