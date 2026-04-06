import attrs

from liblaf.pretty._trace import TracedObject, TracedRef, TraceId

from ._context import TraceContext
from ._spec import Spec


@attrs.define
class SpecObject[T: TracedObject | TracedRef](Spec[T]):
    ref: TraceId = attrs.field(kw_only=True)
    referencable: bool = attrs.field(default=True, kw_only=True)

    def visited(self, ctx: TraceContext) -> TracedRef | None:
        if not self.referencable or self.ref.id_ not in ctx.traced:
            return None
        anchor: TracedObject = ctx.traced[self.ref.id_]
        anchor.annotated = True
        return TracedRef(self.ref)
