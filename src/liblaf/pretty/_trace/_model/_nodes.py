from __future__ import annotations

import abc
from typing import TYPE_CHECKING

import attrs
from rich.text import Text

from liblaf.pretty._compile import Item, Lowered, LoweredContainer, LoweredLeaf

from ._items import TracedItem

if TYPE_CHECKING:
    from liblaf.pretty._lower._lowerer import Lowerer
    from liblaf.pretty._trace._helpers._items import ItemSpec


@attrs.define
class TracedNode(abc.ABC):
    obj_id: int
    cls: type
    referable: bool
    appearance_count: int = attrs.field(default=1, kw_only=True)

    def lower(
        self,
        lowerer: Lowerer,
        *,
        inline_repeat: bool,
        ancestors: tuple[int, ...],
        annotate: bool = False,
    ) -> Lowered:
        lowered = self._lower_body(
            lowerer, inline_repeat=inline_repeat, ancestors=ancestors
        )
        if annotate:
            lowered.annotation = lowerer.ctx.reference_formatter.anchor_annotation(
                self.cls, self.obj_id, lowerer.ctx.typenames
            )
        return lowered

    @abc.abstractmethod
    def _lower_body(
        self,
        lowerer: Lowerer,
        *,
        inline_repeat: bool,
        ancestors: tuple[int, ...],
    ) -> Lowered:
        raise NotImplementedError


@attrs.define
class TracedLeafNode(TracedNode):
    value: Text = attrs.field(converter=lambda value: value.copy())

    def _lower_body(
        self,
        lowerer: Lowerer,
        *,
        inline_repeat: bool,
        ancestors: tuple[int, ...],
    ) -> LoweredLeaf:
        del lowerer, inline_repeat, ancestors
        return LoweredLeaf(self.value.copy())


@attrs.define
class TracedContainerNode(TracedNode):
    open_brace: str
    close_brace: str
    empty_open_brace: str
    empty_close_brace: str
    show_type_name: bool = attrs.field(default=False)
    trailing_comma_single: bool = attrs.field(default=False)
    source_items: tuple[ItemSpec, ...] = attrs.field(factory=tuple, repr=False)
    items: tuple[TracedItem, ...] = attrs.field(factory=tuple)
    expanded: bool = attrs.field(default=False)

    def _lower_body(
        self,
        lowerer: Lowerer,
        *,
        inline_repeat: bool,
        ancestors: tuple[int, ...],
    ) -> Lowered:
        if not self.items:
            return LoweredLeaf(
                Text.assemble(
                    *self._type_name(lowerer),
                    (self.empty_open_brace, "repr.tag_start"),
                    (self.empty_close_brace, "repr.tag_end"),
                )
            )
        child_ancestors = (*ancestors, self.obj_id)
        items: list[Item] = [
            item.lower(lowerer, inline_repeat=inline_repeat, ancestors=child_ancestors)
            for item in self.items
        ]
        return LoweredContainer(
            begin=Text.assemble(
                *self._type_name(lowerer), (self.open_brace, "repr.tag_start")
            ),
            end=Text(self.close_brace, "repr.tag_end"),
            items=items,
            indent=lowerer.ctx.indent,
        )

    def _type_name(self, lowerer: Lowerer) -> tuple[tuple[str, str], ...]:
        if not self.show_type_name:
            return ()
        return ((lowerer.ctx.typenames[self.cls], "repr.tag_name"),)
