from collections import Counter
from collections.abc import Callable
from typing import NamedTuple

import attrs

from liblaf.pretty._conf import PrettyOptions, config
from liblaf.pretty._trace import Traced, TracedObject, TracedRef

from ._object import SpecObject
from ._spec import Spec


class Pending[T: Traced](NamedTuple):
    spec: Spec[T]
    depth: int
    attach: Callable[[T], None]


@attrs.define
class TraceContext:
    options: PrettyOptions = attrs.field(factory=config.dump)
    queue: list[Pending] = attrs.field(factory=list)
    traced: dict[int, TracedObject] = attrs.field(factory=dict)

    def enqueue[T: Traced](
        self, spec: Spec[T], depth: int, attach: Callable[[T], None]
    ) -> None:
        self.queue.append(Pending(spec, depth, attach))

    def visit(self, spec: SpecObject) -> TracedRef | None:
        if spec.ref is None or spec.ref.id_ not in self.traced:
            return None
        anchor: TracedObject = self.traced[spec.ref.id_]
        anchor.ref = spec.ref
        return TracedRef(spec.ref)
