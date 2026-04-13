from __future__ import annotations

import enum
from collections import deque
from collections.abc import Generator, Iterable
from typing import TYPE_CHECKING, Any

import attrs
from rich.text import Text

from liblaf.pretty._conf import PrettyOptions, config
from liblaf.pretty._trace import TracedNode, TracedObject

from ._base import Child

if TYPE_CHECKING:
    from ._item_base import WrappedItem
    from ._node_base import WrappedNode


class _TruncatedType(enum.Enum):
    TRUNCATED = enum.auto()


TRUNCATED: Any = _TruncatedType.TRUNCATED


@attrs.define
class TraceContext:
    depth: int = 0
    options: PrettyOptions = attrs.field(factory=config.dump)
    trace_cache: dict[int, TracedObject] = attrs.field(factory=dict)
    _types: set[type] = attrs.field(factory=set)

    def ellipsis_item(self) -> WrappedItem:
        raise NotImplementedError

    def trace(self, root: WrappedNode) -> TracedNode:
        children, traced_root = root.trace(self)
        queue: deque[Child] = deque(children)
        while queue:
            obj, self.depth, attach = queue.popleft()
            wrapped: WrappedNode = self.wrap(obj)
            children, traced = wrapped.trace(self)
            queue.extend(children)
            if attach is not None:
                attach(traced)
        return traced_root

    def container(
        self, obj: Any, begin: Text, children: Iterable[WrappedItem], end: Text
    ) -> WrappedNode:
        raise NotImplementedError

    def truncate_dict[K, V](
        self, items: Iterable[tuple[K, V]]
    ) -> Generator[tuple[K, V]]:
        for i, item in enumerate(items):
            if self.depth >= self.options.max_level or i >= self.options.max_dict:
                yield TRUNCATED, TRUNCATED
                break
            yield item

    def truncate_fields[T](
        self, fields: Iterable[tuple[str, T]]
    ) -> Generator[tuple[str, T]]:
        for item in fields:
            if self.depth >= self.options.max_level:
                yield TRUNCATED, TRUNCATED
                break
            yield item

    def truncate_list[T](self, items: Iterable[T]) -> Generator[T]:
        for i, item in enumerate(items):
            if self.depth >= self.options.max_level or i >= self.options.max_list:
                yield TRUNCATED
                break
            yield item

    def wrap(self, obj: Any) -> WrappedNode:
        raise NotImplementedError

    def wrap_key_value(self, key: Any, value: Any) -> WrappedItem:
        raise NotImplementedError

    def wrap_name_value(self, name: str | Text, value: Any) -> WrappedItem:
        raise NotImplementedError

    def wrap_positional_value(self, value: Any) -> WrappedItem:
        if value is TRUNCATED:
            return self.ellipsis_item()
        raise NotImplementedError


def _wrap_list(obj: list, ctx: TraceContext) -> WrappedNode:
    children: list[WrappedItem] = [
        ctx.wrap_positional_value(item) for item in ctx.truncate_list(obj)
    ]
    return ctx.container(obj, begin=Text("["), children=children, end=Text("]"))
