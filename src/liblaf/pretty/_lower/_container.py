from collections.abc import Generator, Sequence
from typing import override

import attrs
from rich.text import Text

from liblaf.pretty._compile import (
    BREAK,
    COLON,
    COMMA,
    EQUAL,
    INDENT,
    Item,
    ItemKeyValue,
    ItemValue,
    Lowered,
    LoweredContainer,
    LoweredLeaf,
)

from ._base import LowerContext, Traced
from ._reference import TracedReferent

type TracedItem = Traced | tuple[str, Traced] | tuple[Traced, Traced]


@attrs.define
class TracedContainer(TracedReferent):
    children: Sequence[TracedItem]

    open_brace: str = attrs.field(kw_only=True)
    close_brace: str = attrs.field(kw_only=True)

    def _default_empty_open_brace(self) -> str:
        return self.open_brace[0]

    empty_open_brace: str = attrs.field(
        default=attrs.Factory(_default_empty_open_brace, takes_self=True), kw_only=True
    )

    def _default_empty_close_brace(self) -> str:
        return self.close_brace[-1]

    empty_close_brace: str = attrs.field(
        default=attrs.Factory(_default_empty_close_brace, takes_self=True), kw_only=True
    )

    space: Text = attrs.field(default=BREAK, kw_only=True)
    comma: Text = attrs.field(default=COMMA, kw_only=True)
    indent: Text = attrs.field(default=INDENT, kw_only=True)
    force_comma_if_single: bool = attrs.field(default=False, kw_only=True)

    @override
    def lower_referent(self, ctx: LowerContext) -> Lowered:
        items: list[Item] = list(self.lower_items(ctx))
        if not items:
            return LoweredLeaf(
                Text.assemble(
                    (ctx.typenames[self.cls], "repr.tag_name"),
                    (self.empty_open_brace, "repr.tag_start"),
                    (self.empty_close_brace, "repr.tag_end"),
                )
            )
        begin: Text = Text.assemble(
            (ctx.typenames[self.cls], "repr.tag_name"),
            (self.open_brace, "repr.tag_start"),
        )
        end: Text = Text(self.close_brace, "repr.tag_end")
        for i, item in enumerate(items):
            if i > 0:
                item.prefix = self.space
            if i < len(items) - 1 or (self.force_comma_if_single and len(items) == 1):
                item.suffix = self.comma
        return LoweredContainer(begin=begin, end=end, items=items, indent=self.indent)

    def lower_items(self, ctx: LowerContext) -> Generator[Item]:
        for child in self.children:
            match child:
                case Traced():
                    yield ItemValue(child.lower(ctx))
                case (str() as name, Traced() as value):
                    yield ItemKeyValue(
                        key=LoweredLeaf(Text(name, "repr.attrib_name")),
                        value=value.lower(ctx),
                        sep=EQUAL,
                    )
                case (Traced() as key, Traced() as value):
                    yield ItemKeyValue(
                        key=key.lower(ctx), value=value.lower(ctx), sep=COLON
                    )
                case _:
                    raise ValueError(child)
