from collections.abc import Iterable
from typing import Any, override

import attrs

from liblaf.pretty.stages.traced import TracedNode

from ._base import WrappedChild
from ._context import TraceContext
from ._node_base import WrappedNode


@attrs.define
class WrappedLazy(WrappedNode):
    obj: Any
    _cache: WrappedNode | None = attrs.field(default=None, init=False)

    @override
    def trace(self, ctx: TraceContext) -> tuple[Iterable[WrappedChild], TracedNode]:
        if self._cache is None:
            self._cache = ctx.wrap_eager(self.obj)
        return self._cache.trace(ctx)
