from typing import Self, override

import attrs
from rich.text import Text

from liblaf.pretty._const import ELLIPSIS
from liblaf.pretty._trace import TracedLeaf, TracedRef, TraceId

from ._context import TraceContext
from ._object import SpecObject


@attrs.define
class SpecLeaf(SpecObject[TracedLeaf | TracedRef]):
    value: Text

    @classmethod
    def ellipsis(cls) -> Self:
        return cls(ELLIPSIS, referencable=False, ref=TraceId.from_obj(...))

    @override
    def trace(self, ctx: TraceContext, depth: int) -> TracedLeaf | TracedRef:
        if (traced := self.visited(ctx)) is not None:
            return traced
        traced: TracedLeaf = TracedLeaf(self.value, ref=self.ref)
        ctx.traced[self.ref.id_] = traced
        return traced
