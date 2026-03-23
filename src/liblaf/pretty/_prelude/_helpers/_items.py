from __future__ import annotations

import abc
from collections.abc import Callable
from typing import TYPE_CHECKING

import attrs

from liblaf.pretty._trace._core._items import (
    TracedEntryItem,
    TracedFieldItem,
    TracedValueItem,
)

from ._common import PrettyChild

if TYPE_CHECKING:
    from liblaf.pretty._trace._core._items import LowerableChild, TracedItem


@attrs.frozen
class ItemSpec(abc.ABC):
    @abc.abstractmethod
    def trace_item(
        self,
        *,
        prefix_break: bool,
        trailing_comma: bool,
        slot_index: int,
        trace_child: Callable[[PrettyChild, int], tuple[LowerableChild, int]],
    ) -> tuple[TracedItem, int]:
        raise NotImplementedError


@attrs.frozen
class ValueItemSpec(ItemSpec):
    child: PrettyChild

    def trace_item(
        self,
        *,
        prefix_break: bool,
        trailing_comma: bool,
        slot_index: int,
        trace_child: Callable[[PrettyChild, int], tuple[LowerableChild, int]],
    ) -> tuple[TracedItem, int]:
        child, slot_index = trace_child(self.child, slot_index)
        return (
            TracedValueItem(
                child,
                prefix_break=prefix_break,
                trailing_comma=trailing_comma,
            ),
            slot_index,
        )


@attrs.frozen
class EntryItemSpec(ItemSpec):
    key: PrettyChild
    value: PrettyChild

    def trace_item(
        self,
        *,
        prefix_break: bool,
        trailing_comma: bool,
        slot_index: int,
        trace_child: Callable[[PrettyChild, int], tuple[LowerableChild, int]],
    ) -> tuple[TracedItem, int]:
        key, slot_index = trace_child(self.key, slot_index)
        value, slot_index = trace_child(self.value, slot_index)
        return (
            TracedEntryItem(
                key,
                value,
                prefix_break=prefix_break,
                trailing_comma=trailing_comma,
            ),
            slot_index,
        )


@attrs.frozen
class FieldItemSpec(ItemSpec):
    name: str
    value: PrettyChild

    def trace_item(
        self,
        *,
        prefix_break: bool,
        trailing_comma: bool,
        slot_index: int,
        trace_child: Callable[[PrettyChild, int], tuple[LowerableChild, int]],
    ) -> tuple[TracedItem, int]:
        value, slot_index = trace_child(self.value, slot_index)
        return (
            TracedFieldItem(
                name=self.name,
                value=value,
                prefix_break=prefix_break,
                trailing_comma=trailing_comma,
            ),
            slot_index,
        )
