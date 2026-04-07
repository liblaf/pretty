from __future__ import annotations

from typing import TYPE_CHECKING, Self, override

import attrs
from rich.text import Text

from liblaf.pretty._const import ELLIPSIS, EMPTY
from liblaf.pretty._lower import LoweredContainer, LoweredLeaf

from ._base import Traced
from ._context import LowerContext
from ._ref import Ref

if TYPE_CHECKING:
    from ._item import TracedItem


@attrs.define
class TracedContainer(Traced):
    begin: Text
    items: list[TracedItem]
    end: Text
    indent: Text
    ref: Ref
    has_ref: bool = attrs.field(default=False, kw_only=True)

    def _default_empty(self) -> Text:
        return self.begin + self.end

    empty: Text = attrs.field(
        default=attrs.Factory(_default_empty, takes_self=True), kw_only=True
    )

    @override
    def lower(self, ctx: LowerContext) -> LoweredContainer | LoweredLeaf:
        annotation: Text = _make_annotation(ctx, self)
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


@attrs.define
class TracedLeaf(Traced):
    value: Text
    ref: Ref
    has_ref: bool = attrs.field(default=False, kw_only=True)

    @classmethod
    def ellipsis(cls) -> Self:
        return cls(ELLIPSIS, has_ref=False, ref=Ref.from_obj(...))

    @override
    def lower(self, ctx: LowerContext) -> LoweredLeaf:
        annotation: Text = _make_annotation(ctx, self)
        return LoweredLeaf(self.value, annotation=annotation)


@attrs.define
class TracedRef(Traced):
    ref: Ref

    @override
    def lower(self, ctx: LowerContext) -> LoweredLeaf:
        typename: str = ctx.get_ref_typename(self.ref.cls)
        return LoweredLeaf(
            Text.assemble(
                ("<", "repr.tag_start"),
                (typename, "repr.tag_name"),
                (f" @ {self.ref.id_:x}", "repr.tag_contents"),
                (">", "repr.tag_end"),
            )
        )


type TracedNode = TracedContainer | TracedLeaf | TracedRef


def _make_annotation(ctx: LowerContext, traced: TracedContainer | TracedLeaf) -> Text:
    if not traced.has_ref:
        return EMPTY
    typename: str = ctx.get_ref_typename(traced.ref.cls)
    return Text(f"  # <{typename} @ {traced.ref.id_:x}>", "dim")
