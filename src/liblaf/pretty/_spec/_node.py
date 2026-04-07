from __future__ import annotations

import abc
from collections.abc import Iterable
from typing import TYPE_CHECKING, Self, override

import attrs
from rich.text import Text

from liblaf.pretty._const import ELLIPSIS
from liblaf.pretty._trace import (
    Ref,
    TracedContainer,
    TracedLeaf,
    TracedNode,
    TracedRef,
    TracedValueItem,
)

from ._base import Spec

if TYPE_CHECKING:
    from ._context import TraceContext
    from ._item import SpecItem


class SpecNode(Spec):
    @override
    @abc.abstractmethod
    def trace(self, ctx: TraceContext, depth: int) -> TracedNode: ...


@attrs.define
class SpecContainer(SpecNode):
    begin: Text
    items: Iterable[SpecItem]
    end: Text
    indent: Text
    ref: Ref
    referencable: bool = attrs.field(default=True, kw_only=True)

    def _default_empty(self) -> Text:
        return self.begin + self.end

    empty: Text = attrs.field(
        default=attrs.Factory(_default_empty, takes_self=True), kw_only=True
    )

    @override
    def trace(self, ctx: TraceContext, depth: int) -> TracedNode:
        if (traced := _visit(ctx, self)) is not None:
            return traced
        traced: TracedContainer = TracedContainer(
            begin=self.begin,
            items=[],
            end=self.end,
            indent=self.indent,
            empty=self.empty,
            ref=self.ref,
        )
        if depth < ctx.options.max_level:
            for item in self.items:
                traced.items.append(item.trace(ctx, depth + 1))
        else:
            traced.items = [TracedValueItem.ellipsis()]
        ctx.traced[self.ref.id_] = traced
        return traced


@attrs.define
class SpecLeaf(SpecNode):
    value: Text
    ref: Ref
    referencable: bool = attrs.field(default=False, kw_only=True)

    @classmethod
    def ellipsis(cls) -> Self:
        return cls(ELLIPSIS, ref=Ref.from_obj(...), referencable=False)

    @override
    def trace(self, ctx: TraceContext, depth: int) -> TracedLeaf | TracedRef:
        if (traced := _visit(ctx, self)) is not None:
            return traced
        traced = TracedLeaf(self.value, ref=self.ref)
        ctx.traced[self.ref.id_] = traced
        return traced


def _visit(ctx: TraceContext, spec: SpecContainer | SpecLeaf) -> TracedRef | None:
    if spec.referencable:
        ctx.types_.add(spec.ref.cls)
        if (traced := ctx.traced.get(spec.ref.id_)) is not None:
            traced.has_ref = True
            return TracedRef(spec.ref)
    return None
