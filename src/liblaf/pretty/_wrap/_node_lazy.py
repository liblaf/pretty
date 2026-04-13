from __future__ import annotations

from collections.abc import Callable, Iterable
from typing import TYPE_CHECKING, override

import attrs

from liblaf.pretty._trace import TracedNode

from ._base import Child
from ._node_base import WrappedNode

if TYPE_CHECKING:
    from ._context import TraceContext


@attrs.define
class WrappedLazy(WrappedNode):
    factory: Callable[[TraceContext], WrappedNode]
    _cache: WrappedNode | None = attrs.field(default=None, init=False)

    @override
    def trace(self, ctx: TraceContext) -> tuple[Iterable[Child], TracedNode]:
        if self._cache is None:
            self._cache = self.factory(ctx)
        return self._cache.trace(ctx)
