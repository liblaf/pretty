from __future__ import annotations

from typing import TYPE_CHECKING, Any

import attrs

from liblaf.pretty._conf import PrettyOptions, config
from liblaf.pretty.stages.traced import TracedObject

if TYPE_CHECKING:
    from ._node_base import WrappedNode


@attrs.define
class TraceContext:
    depth: int = 0
    options: PrettyOptions = attrs.field(factory=config.dump)
    trace_cache: dict[int, TracedObject] = attrs.field(factory=dict)
    _types: set[type] = attrs.field(factory=set)

    def wrap_eager(self, obj: Any) -> WrappedNode:
        raise NotImplementedError
