from __future__ import annotations

import functools
import types
from collections import Counter, deque
from collections.abc import Callable

from rich.text import Text

from liblaf.pretty._options import PrettyOptions
from liblaf.pretty._spec import (
    Spec,
    SpecContainer,
    SpecField,
    SpecItem,
    SpecKeyValue,
    SpecLeaf,
    SpecValue,
)

from ._model import (
    Traced,
    TracedContainer,
    TracedDocument,
    TracedField,
    TracedKeyValue,
    TracedLeaf,
    TracedReference,
    TracedValue,
)
from ._typenames import disambiguate_typenames

_ELLIPSIS = Text("...", "repr.ellipsis")

type Attach = Callable[[Traced], None]


def build_traced(spec: Spec, options: PrettyOptions) -> TracedDocument:
    counts: Counter[int] = Counter()
    types_seen: set[type] = set()
    root_holder: list[Traced | None] = [None]
    queue: deque[tuple[int, Spec, Attach]] = deque(
        [(0, spec, functools.partial(_set_root, root_holder))]
    )

    while queue:
        depth, current, attach = queue.popleft()
        types_seen.add(current.cls)
        obj_id: int | None = _referable_id(current)
        if obj_id is not None:
            counts[obj_id] += 1
            if counts[obj_id] > 1:
                attach(TracedReference(cls=current.cls, obj_id=obj_id))
                continue

        _trace_spec(
            current,
            obj_id=obj_id,
            attach=attach,
            depth=depth,
            options=options,
            queue=queue,
        )

    root: Traced | None = root_holder[0]
    if root is None:
        msg = "trace produced no root node"
        raise RuntimeError(msg)
    return TracedDocument(
        root=root,
        obj_id_counts=counts,
        typenames=disambiguate_typenames(types_seen),
    )


@functools.singledispatch
def _trace_spec(
    current: Spec,
    *,
    _obj_id: int | None,
    _attach: Attach,
    _depth: int,
    _options: PrettyOptions,
    _queue: deque[tuple[int, Spec, Attach]],
) -> None:
    msg = f"unsupported spec: {type(current)!r}"
    raise TypeError(msg)


@_trace_spec.register
def _trace_leaf(
    current: SpecLeaf,
    *,
    obj_id: int | None,
    attach: Attach,
    depth: int,
    options: PrettyOptions,
    queue: deque[tuple[int, Spec, Attach]],
) -> None:
    del depth, options, queue
    attach(
        TracedLeaf(
            cls=current.cls,
            obj_id=obj_id,
            text=current.text,
        )
    )


@_trace_spec.register
def _trace_container(
    current: SpecContainer,
    *,
    obj_id: int | None,
    attach: Attach,
    depth: int,
    options: PrettyOptions,
    queue: deque[tuple[int, Spec, Attach]],
) -> None:
    node = TracedContainer(
        cls=current.cls,
        obj_id=obj_id,
        begin=current.begin,
        end=current.end,
        empty=current.empty_text(),
        force_comma_if_single=current.force_comma_if_single(),
    )
    attach(node)
    if depth >= options.max_level:
        node.items.append(
            TracedValue(value=TracedLeaf(cls=types.EllipsisType, text=_ELLIPSIS))
        )
        return

    limit: int = current.max_items(options)
    for index, item in enumerate(current.iter_children()):
        if index >= limit:
            node.items.append(
                TracedValue(value=TracedLeaf(cls=types.EllipsisType, text=_ELLIPSIS))
            )
            break
        _enqueue_item(item, queue=queue, container=node, depth=depth + 1)


@functools.singledispatch
def _enqueue_item(
    item: SpecItem,
    *,
    _queue: deque[tuple[int, Spec, Attach]],
    _container: TracedContainer,
    _depth: int,
) -> None:
    msg = f"unsupported spec item: {type(item)!r}"
    raise TypeError(msg)


@_enqueue_item.register
def _enqueue_value(
    item: SpecValue,
    *,
    queue: deque[tuple[int, Spec, Attach]],
    container: TracedContainer,
    depth: int,
) -> None:
    traced_item = TracedValue()
    container.items.append(traced_item)
    queue.append(
        (depth, item.value, functools.partial(_set_attr, traced_item, "value"))
    )


@_enqueue_item.register
def _enqueue_field(
    item: SpecField,
    *,
    queue: deque[tuple[int, Spec, Attach]],
    container: TracedContainer,
    depth: int,
) -> None:
    traced_item = TracedField(name=item.name)
    container.items.append(traced_item)
    queue.append(
        (depth, item.value, functools.partial(_set_attr, traced_item, "value"))
    )


@_enqueue_item.register
def _enqueue_key_value(
    item: SpecKeyValue,
    *,
    queue: deque[tuple[int, Spec, Attach]],
    container: TracedContainer,
    depth: int,
) -> None:
    traced_item = TracedKeyValue()
    container.items.append(traced_item)
    queue.append((depth, item.key, functools.partial(_set_attr, traced_item, "key")))
    queue.append(
        (depth, item.value, functools.partial(_set_attr, traced_item, "value"))
    )


def _referable_id(spec: Spec) -> int | None:
    if not spec.referable or spec.id_ is None:
        return None
    return spec.id_


def _set_attr(obj: object, name: str, value: Traced) -> None:
    setattr(obj, name, value)


def _set_root(root_holder: list[Traced | None], value: Traced) -> None:
    root_holder[0] = value
