from __future__ import annotations

import abc
from typing import TYPE_CHECKING, Protocol

import attrs
from rich.text import Text

from ..._compile import BREAK, COLON, COMMA, EMPTY, EQUAL
from ..._compile import Item, ItemKeyValue, ItemValue, LoweredLeaf

if TYPE_CHECKING:
    from ..._compile import Lowered
    from ..._lower._lowerer import Lowerer

class LowerableChild(Protocol):
    def lower(
        self,
        lowerer: Lowerer,
        *,
        inline_repeat: bool,
        ancestors: tuple[int, ...],
    ) -> Lowered: ...

@attrs.define
class TracedLiteral:
    value: Text = attrs.field(converter=lambda value: value.copy())

    def lower(
        self,
        _lowerer: Lowerer,
        *,
        inline_repeat: bool,
        ancestors: tuple[int, ...],
    ) -> LoweredLeaf:
        del inline_repeat, ancestors
        return LoweredLeaf(self.value.copy())

@attrs.define
class TracedItem(abc.ABC):
    prefix_break: bool = attrs.field(default=False, kw_only=True)
    trailing_comma: bool = attrs.field(default=False, kw_only=True)

    @property
    def prefix(self) -> Text:
        return BREAK if self.prefix_break else EMPTY

    @property
    def suffix(self) -> Text:
        return COMMA if self.trailing_comma else EMPTY

    @abc.abstractmethod
    def lower(
        self,
        lowerer: Lowerer,
        *,
        inline_repeat: bool,
        ancestors: tuple[int, ...],
    ) -> Item:
        raise NotImplementedError

@attrs.define
class TracedValueItem(TracedItem):
    child: LowerableChild = attrs.field()

    def lower(
        self,
        lowerer: Lowerer,
        *,
        inline_repeat: bool,
        ancestors: tuple[int, ...],
    ) -> ItemValue:
        return ItemValue(
            self.child.lower(
                lowerer, inline_repeat=inline_repeat, ancestors=ancestors
            ),
            prefix=self.prefix,
            suffix=self.suffix,
        )

@attrs.define
class TracedEntryItem(TracedItem):
    key: LowerableChild = attrs.field()
    value: LowerableChild = attrs.field()

    def lower(
        self,
        lowerer: Lowerer,
        *,
        inline_repeat: bool,
        ancestors: tuple[int, ...],
    ) -> ItemKeyValue:
        return ItemKeyValue(
            key=self.key.lower(
                lowerer, inline_repeat=inline_repeat, ancestors=ancestors
            ),
            value=self.value.lower(
                lowerer, inline_repeat=inline_repeat, ancestors=ancestors
            ),
            sep=COLON,
            prefix=self.prefix,
            suffix=self.suffix,
        )

@attrs.define
class TracedFieldItem(TracedItem):
    name: str = attrs.field()
    value: LowerableChild = attrs.field()

    def lower(
        self,
        lowerer: Lowerer,
        *,
        inline_repeat: bool,
        ancestors: tuple[int, ...],
    ) -> ItemKeyValue:
        return ItemKeyValue(
            key=LoweredLeaf(Text(self.name, "repr.attrib_name")),
            value=self.value.lower(
                lowerer, inline_repeat=inline_repeat, ancestors=ancestors
            ),
            sep=EQUAL,
            prefix=self.prefix,
            suffix=self.suffix,
        )
