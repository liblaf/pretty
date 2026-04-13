from collections.abc import Callable
from typing import Any

import attrs

from liblaf.pretty.stages.wrapped import WrappedNode

from ._context import TraceContext


@attrs.define
class PrettyRegistry:
    def __call__(self, obj: Any, ctx: TraceContext) -> WrappedNode:
        raise NotImplementedError

    def register_func(
        self, func: Callable[[Any, TraceContext], WrappedNode]
    ) -> Callable[[Any, TraceContext], WrappedNode]:
        raise NotImplementedError
        return func
