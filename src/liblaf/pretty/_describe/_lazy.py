from __future__ import annotations

from typing import TYPE_CHECKING, Protocol, override

import attrs

from liblaf.pretty._spec import SpecNode, TraceContext
from liblaf.pretty._trace import TracedNode

if TYPE_CHECKING:
    from ._context import DescribeContext


@attrs.define
class LazySpec(SpecNode):
    class Factory(Protocol):
        def __call__(self, ctx: DescribeContext, depth: int, /) -> SpecNode: ...

    describe_ctx: DescribeContext = attrs.field(repr=False)
    factory: Factory = attrs.field(repr=False)
    _spec: SpecNode | None = attrs.field(default=None, init=False, repr=False)

    @override
    def trace(self, ctx: TraceContext, depth: int) -> TracedNode:
        if self._spec is None:
            self._spec = self.factory(self.describe_ctx, depth)
        return self._spec.trace(ctx, depth)
