from typing import override

import attrs
from rich.text import Text

from liblaf.pretty._trace import TracedLeaf, TracedObject, TracedRef

from ._context import TraceContext
from ._object import SpecObject


@attrs.define
class SpecLeaf(SpecObject[TracedLeaf | TracedRef]):
    value: Text

    @override
    def trace(self, ctx: TraceContext, depth: int) -> TracedLeaf | TracedRef:
        if self.ref is not None and self.ref.id_ in ctx.traced:
            anchor: TracedObject = ctx.traced[self.ref.id_]
            anchor.ref = self.ref
            return TracedRef(self.ref)
        traced = TracedLeaf(self.value)
        if self.ref is not None:
            ctx.traced[self.ref.id_] = traced
        return traced
