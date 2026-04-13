import enum
from collections import deque
from collections.abc import Generator, Iterable
from typing import Any, override

import attrs
from rich.text import Text

from liblaf.pretty.common import ObjectIdentifier
from liblaf.pretty.literals import COMMA, SPACE
from liblaf.pretty.stages.traced import TracedNode
from liblaf.pretty.stages.wrapped import (
    TraceContext,
    WrappedChild,
    WrappedContainer,
    WrappedItem,
    WrappedKeyValueItem,
    WrappedLazy,
    WrappedLeaf,
    WrappedNameValueItem,
    WrappedNode,
    WrappedPositionalItem,
)


class _TruncatedType(enum.Enum):
    TRUNCATED = enum.auto()


TRUNCATED: Any = _TruncatedType.TRUNCATED


@attrs.define
class TraceContext(TraceContext):
    wrap_cache: dict[int, WrappedNode] = attrs.field(factory=dict)

    def add_separators(self, items: Iterable[WrappedItem]) -> list[WrappedItem]:
        items: list[WrappedItem] = list(items)
        for i, item in enumerate(items):
            if i > 0:
                item.prefix = SPACE
            if i < len(items) - 1:
                item.suffix = COMMA
        return items

    def ellipsis_item(self) -> WrappedItem:
        return WrappedPositionalItem.ellipsis()

    def identifier(self, obj: Any) -> ObjectIdentifier:
        return ObjectIdentifier.from_obj(obj)

    def trace(self, root: WrappedNode) -> TracedNode:
        children, traced_root = root.trace(self)
        queue: deque[WrappedChild] = deque(children)
        while queue:
            obj, self.depth, attach = queue.popleft()
            wrapped: WrappedNode = self.wrap_lazy(obj)
            children, traced = wrapped.trace(self)
            queue.extend(children)
            attach(traced)
        return traced_root

    @override
    def wrap_eager(self, obj: Any) -> WrappedNode:
        if (cached := self.wrap_cache.get(id(obj))) is not None:
            return cached
        raise NotImplementedError

    def wrap_lazy(self, obj: Any) -> WrappedLazy:
        return WrappedLazy(obj=obj, identifier=self.identifier(obj))

    # ------------------------------ truncate_* ------------------------------ #

    def truncate_dict[K, V](
        self, items: Iterable[tuple[K, V]]
    ) -> Generator[tuple[K, V]]:
        for i, item in enumerate(items):
            if i >= self.options.max_dict:
                yield TRUNCATED, TRUNCATED
                break
            yield item

    def truncate_list[T](self, items: Iterable[T]) -> Generator[T]:
        for i, item in enumerate(items):
            if i >= self.options.max_list:
                yield TRUNCATED
                break
            yield item

    # ------------------------------ WrappedItem ----------------------------- #

    def key_value(self, key: Any, value: Any) -> WrappedItem:
        if key is TRUNCATED or value is TRUNCATED:
            return self.ellipsis_item()
        return WrappedKeyValueItem(key=self.wrap_lazy(key), value=self.wrap_lazy(value))

    def name_value(self, name: str | Text, value: Any) -> WrappedItem:
        if name is TRUNCATED or value is TRUNCATED:
            return self.ellipsis_item()
        if isinstance(name, str):
            name = Text(name, "repr.attrib_name")
        return WrappedNameValueItem(name=name, value=self.wrap_lazy(value))

    def positional_value(self, value: Any) -> WrappedItem:
        if value is TRUNCATED:
            return self.ellipsis_item()
        return WrappedPositionalItem(value=self.wrap_lazy(value))

    # ------------------------------ WrappedNode ----------------------------- #

    def container(
        self,
        obj: Any,
        begin: Text,
        children: Iterable[WrappedItem],
        end: Text,
        indent: Text | None = None,
        *,
        empty: Text | None = None,
        referencable: bool = True,
    ) -> WrappedContainer:
        if indent is None:
            indent: Text = self.options.indent
        kwargs: dict[str, Any] = {}
        if empty is not None:
            kwargs["empty"] = empty
        return WrappedContainer(
            begin=begin,
            children=children,
            end=end,
            indent=indent,
            identifier=self.identifier(obj),
            referencable=referencable,
            **kwargs,
        )

    def leaf(self, obj: Any, text: Text, *, referencable: bool = True) -> WrappedLeaf:
        return WrappedLeaf(
            value=text, identifier=self.identifier(obj), referencable=referencable
        )
