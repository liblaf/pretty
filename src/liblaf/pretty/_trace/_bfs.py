from __future__ import annotations

import functools
import types
from collections import Counter, deque
from typing import cast

from rich.text import Text

from liblaf.pretty._options import PrettyOptions
from liblaf.pretty._spec import (
    Attach,
    Spec,
    TraceFactory,
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


class _TraceFactory:
    def make_leaf(self, *, cls: type, obj_id: int | None, text: Text) -> TracedLeaf:
        return TracedLeaf(cls=cls, obj_id=obj_id, text=text)

    def make_value_item(self) -> TracedValue:
        return TracedValue()

    def make_field_item(self, *, name: str) -> TracedField:
        return TracedField(name=name)

    def make_key_value_item(self) -> TracedKeyValue:
        return TracedKeyValue()

    def make_container(
        self,
        *,
        cls: type,
        obj_id: int | None,
        begin: Text,
        end: Text,
        empty: Text,
        force_comma_if_single: bool,
    ) -> TracedContainer:
        return TracedContainer(
            cls=cls,
            obj_id=obj_id,
            begin=begin,
            end=end,
            empty=empty,
            force_comma_if_single=force_comma_if_single,
        )

    def make_ellipsis_item(self) -> TracedValue:
        return TracedValue(
            value=TracedLeaf(cls=types.EllipsisType, text=_ELLIPSIS),
        )


def build_traced(spec: Spec, options: PrettyOptions) -> TracedDocument:
    factory = cast("TraceFactory", _TraceFactory())
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

        current.trace(
            obj_id=obj_id,
            attach=attach,
            depth=depth,
            options=options,
            queue=queue,
            factory=factory,
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


def _referable_id(spec: Spec) -> int | None:
    if not spec.referable or spec.id_ is None:
        return None
    return spec.id_


def _set_root(root_holder: list[Traced | None], value: Traced) -> None:
    root_holder[0] = value
