from __future__ import annotations

import abc
from collections.abc import Callable, Iterable
from typing import TYPE_CHECKING, Protocol

import attrs
from rich.text import Text


class TraceContainerLike(Protocol):
    items: list[object]


class TraceFactory(Protocol):
    def make_leaf(self, *, cls: type, obj_id: int | None, text: Text) -> object: ...
    def make_value_item(self) -> object: ...
    def make_field_item(self, *, name: str) -> object: ...
    def make_key_value_item(self) -> object: ...
    def make_container(
        self,
        *,
        cls: type,
        obj_id: int | None,
        begin: Text,
        end: Text,
        empty: Text,
        force_comma_if_single: bool,
    ) -> TraceContainerLike: ...
    def make_ellipsis_item(self) -> object: ...


type Attach = Callable[[object], None]

if TYPE_CHECKING:
    from collections import deque

    from ._options import PrettyOptions


def _to_text(value: Text | str) -> Text:
    if isinstance(value, Text):
        return value.copy()
    return Text(str(value))


def _to_optional_text(value: Text | str | None) -> Text | None:
    if value is None:
        return None
    return _to_text(value)


@attrs.frozen(hash=False)
class Spec:
    cls: type
    id_: int | None = None
    referable: bool = True

    def trace(
        self,
        *,
        obj_id: int | None,
        attach: Attach,
        depth: int,
        options: PrettyOptions,
        queue: deque[tuple[int, Spec, Attach]],
        factory: TraceFactory,
    ) -> None:
        del obj_id, attach, depth, options, queue, factory
        msg = f"unsupported spec: {type(self)!r}"
        raise TypeError(msg)


@attrs.frozen(kw_only=True, hash=False)
class SpecLeaf(Spec):
    text: Text = attrs.field(converter=_to_text)

    def trace(
        self,
        *,
        obj_id: int | None,
        attach: Attach,
        depth: int,
        options: PrettyOptions,
        queue: deque[tuple[int, Spec, Attach]],
        factory: TraceFactory,
    ) -> None:
        del depth, options, queue
        attach(factory.make_leaf(cls=self.cls, obj_id=obj_id, text=self.text))


@attrs.frozen(hash=False)
class SpecItem:
    def enqueue(
        self,
        *,
        queue: deque[tuple[int, Spec, Attach]],
        container: TraceContainerLike,
        depth: int,
        factory: TraceFactory,
    ) -> None:
        del queue, container, depth, factory
        msg = f"unsupported spec item: {type(self)!r}"
        raise TypeError(msg)


@attrs.frozen(hash=False)
class SpecValue(SpecItem):
    value: Spec

    def enqueue(
        self,
        *,
        queue: deque[tuple[int, Spec, Attach]],
        container: TraceContainerLike,
        depth: int,
        factory: TraceFactory,
    ) -> None:
        import functools

        traced_item = factory.make_value_item()
        container.items.append(traced_item)
        queue.append(
            (depth, self.value, functools.partial(setattr, traced_item, "value"))
        )


@attrs.frozen(hash=False)
class SpecField(SpecItem):
    name: str
    value: Spec

    def enqueue(
        self,
        *,
        queue: deque[tuple[int, Spec, Attach]],
        container: TraceContainerLike,
        depth: int,
        factory: TraceFactory,
    ) -> None:
        import functools

        traced_item = factory.make_field_item(name=self.name)
        container.items.append(traced_item)
        queue.append(
            (depth, self.value, functools.partial(setattr, traced_item, "value"))
        )


@attrs.frozen(hash=False)
class SpecKeyValue(SpecItem):
    key: Spec
    value: Spec

    def enqueue(
        self,
        *,
        queue: deque[tuple[int, Spec, Attach]],
        container: TraceContainerLike,
        depth: int,
        factory: TraceFactory,
    ) -> None:
        import functools

        traced_item = factory.make_key_value_item()
        container.items.append(traced_item)
        queue.append((depth, self.key, functools.partial(setattr, traced_item, "key")))
        queue.append(
            (depth, self.value, functools.partial(setattr, traced_item, "value"))
        )


@attrs.frozen(kw_only=True, hash=False)
class SpecContainer(Spec, abc.ABC):
    begin: Text = attrs.field(converter=_to_text)
    end: Text = attrs.field(converter=_to_text)
    empty: Text | None = attrs.field(default=None, converter=_to_optional_text)

    @abc.abstractmethod
    def iter_children(self) -> Iterable[SpecItem]:
        raise NotImplementedError

    def empty_text(self) -> Text:
        if self.empty is not None:
            return self.empty.copy()
        return Text.assemble(self.begin, self.end)

    def force_comma_if_single(self) -> bool:
        return False

    def max_items(self, options: PrettyOptions) -> int:
        return options.max_list

    def trace(
        self,
        *,
        obj_id: int | None,
        attach: Attach,
        depth: int,
        options: PrettyOptions,
        queue: deque[tuple[int, Spec, Attach]],
        factory: TraceFactory,
    ) -> None:
        node = factory.make_container(
            cls=self.cls,
            obj_id=obj_id,
            begin=self.begin,
            end=self.end,
            empty=self.empty_text(),
            force_comma_if_single=self.force_comma_if_single(),
        )
        attach(node)
        if depth >= options.max_level:
            node.items.append(factory.make_ellipsis_item())
            return

        limit: int = self.max_items(options)
        for index, item in enumerate(self.iter_children()):
            if index >= limit:
                node.items.append(factory.make_ellipsis_item())
                break
            item.enqueue(queue=queue, container=node, depth=depth + 1, factory=factory)


class PrettyPrintable(Protocol):
    def __pretty__(self, options: PrettyOptions) -> Spec: ...
