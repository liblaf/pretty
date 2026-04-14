import attrs

from liblaf.pretty.stages.traced import TracedRef

from ._context import TraceContext
from ._node_base import WrappedNode


@attrs.define
class WrappedObject(WrappedNode):
    referencable: bool = attrs.field(default=True, kw_only=True)

    def visit(self, ctx: TraceContext) -> TracedRef | None:
        if self.identifier.cls is not None:
            ctx.types.add(self.identifier.cls)
        if (
            self.referencable
            and self.identifier.id_ is not None
            and (anchor := ctx.trace_cache.get(self.identifier.id_)) is not None
        ):
            anchor.has_ref = True
            return TracedRef(identifier=self.identifier)
        return None
