from __future__ import annotations

from collections import deque
from collections.abc import Callable
from typing import TYPE_CHECKING, NamedTuple

import attrs

from liblaf.pretty._conf import PrettyOptions, config
from liblaf.pretty._trace import LowerContext, Traced, TracedObject

if TYPE_CHECKING:
    from ._spec import Spec


class Pending[T: Traced](NamedTuple):
    spec: Spec[T]
    depth: int
    attach: Callable[[T], None]


@attrs.define
class TraceContext:
    options: PrettyOptions = attrs.field(factory=config.dump)
    queue: deque[Pending] = attrs.field(factory=deque)
    traced: dict[int, TracedObject] = attrs.field(factory=dict)

    def enqueue[T: Traced](
        self, spec: Spec[T], depth: int, attach: Callable[[T], None]
    ) -> None:
        self.queue.append(Pending(spec, depth, attach))

    def finish(self) -> LowerContext:
        # TODO: handle typenames
        return LowerContext(typenames={list: ""})

    def trace[T: Traced](self, spec: Spec[T]) -> T:
        traced: Traced = spec.trace(self, depth=0)
        while self.queue:
            spec, depth, attach = self.queue.popleft()
            attach(spec.trace(self, depth))
        return traced
