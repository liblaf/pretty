from __future__ import annotations

import abc
from collections import deque
from collections.abc import Iterable

import attrs

from liblaf.pretty._trace import Traced

from ._item import SpecItem
from ._item_entry import SpecItemEntry
from ._item_field import SpecItemField
from ._item_value import SpecItemValue
from ._spec import Spec
from ._spec_container import SpecContainer
from ._spec_leaf import SpecLeaf


class TraceContext:
    pass


class Pending(abc.ABC):
    @abc.abstractmethod
    def visit(self, ctx: TraceContext) -> Iterable[Pending]: ...

    def finish(self, ctx: TraceContext) -> None:  # noqa: B027
        pass


@attrs.frozen
class PendingSpec(Pending):
    spec: Spec


class PendingSpecLeaf(PendingSpec):
    spec: SpecLeaf


def trace(spec: Spec, ctx: TraceContext) -> Traced:
    queue: deque[Pending] = deque([PendingSpec(spec)])
    while queue:
        pending: Pending = queue.popleft()
        queue.extend(pending.visit(ctx))
        pending.finish(ctx)
