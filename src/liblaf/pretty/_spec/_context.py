from __future__ import annotations

from collections import deque
from collections.abc import Callable
from typing import TYPE_CHECKING, NamedTuple

import attrs

from liblaf.pretty._conf import PrettyOptions, config
from liblaf.pretty._trace import LowerContext, TracedContainer, TracedLeaf, TracedNode

if TYPE_CHECKING:
    from ._node import SpecNode


class Pending(NamedTuple):
    spec: SpecNode
    depth: int
    attach: Callable[[TracedNode], None]


@attrs.define
class TraceContext:
    options: PrettyOptions = attrs.field(factory=config.dump)
    queue: deque[Pending] = attrs.field(factory=deque)
    traced: dict[int, TracedContainer | TracedLeaf] = attrs.field(factory=dict)

    def enqueue(
        self, spec: SpecNode, depth: int, attach: Callable[[TracedNode], None]
    ) -> None:
        self.queue.append(Pending(spec, depth, attach))

    def finish(self) -> LowerContext:
        # TODO: handle typenames
        return LowerContext(typenames={list: ""})

    def trace(self, spec: SpecNode, depth: int = 0) -> TracedNode:
        traced: TracedNode = spec.trace(self, depth=depth)
        while self.queue:
            spec, depth, attach = self.queue.popleft()
            attach(spec.trace(self, depth=depth))
        return traced
