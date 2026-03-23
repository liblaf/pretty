from __future__ import annotations

import abc

import attrs
from rich.text import Text

from ._common import copy_text
from ._items import ItemSpec


@attrs.frozen
class PrettySpec(abc.ABC):
    referable: bool = attrs.field(default=True, kw_only=True)

    @abc.abstractmethod
    def make_node(self, *, obj_id: int, cls: type) -> object:
        raise NotImplementedError


@attrs.frozen
class LiteralSpec(PrettySpec):
    value: Text = attrs.field(converter=copy_text)
    referable: bool = attrs.field(default=False, init=False)

    def make_node(self, *, obj_id: int, cls: type) -> object:
        from ..._trace._core._nodes import TracedLeafNode

        return TracedLeafNode(obj_id=obj_id, cls=cls, referable=False, value=self.value)

    def trace_child(self) -> object:
        from ..._trace._core._items import TracedLiteral

        return TracedLiteral(self.value)


@attrs.frozen
class LeafSpec(PrettySpec):
    value: Text = attrs.field(converter=copy_text)

    def make_node(self, *, obj_id: int, cls: type) -> object:
        from ..._trace._core._nodes import TracedLeafNode

        return TracedLeafNode(
            obj_id=obj_id,
            cls=cls,
            referable=self.referable,
            value=self.value,
        )


@attrs.frozen
class ContainerSpec(PrettySpec):
    items: tuple[ItemSpec, ...] = attrs.field(converter=tuple)
    open_brace: str = attrs.field(kw_only=True)
    close_brace: str = attrs.field(kw_only=True)
    show_type_name: bool = attrs.field(default=False, kw_only=True)
    trailing_comma_single: bool = attrs.field(default=False, kw_only=True)

    def _default_empty_open_brace(self) -> str:
        return self.open_brace[0] if self.open_brace else ""

    empty_open_brace: str = attrs.field(
        default=attrs.Factory(_default_empty_open_brace, takes_self=True), kw_only=True
    )

    def _default_empty_close_brace(self) -> str:
        return self.close_brace[-1] if self.close_brace else ""

    empty_close_brace: str = attrs.field(
        default=attrs.Factory(_default_empty_close_brace, takes_self=True), kw_only=True
    )

    def make_node(self, *, obj_id: int, cls: type) -> object:
        from ..._trace._core._nodes import TracedContainerNode

        return TracedContainerNode(
            obj_id=obj_id,
            cls=cls,
            referable=self.referable,
            open_brace=self.open_brace,
            close_brace=self.close_brace,
            empty_open_brace=self.empty_open_brace,
            empty_close_brace=self.empty_close_brace,
            show_type_name=self.show_type_name,
            trailing_comma_single=self.trailing_comma_single,
            source_items=self.items,
        )
