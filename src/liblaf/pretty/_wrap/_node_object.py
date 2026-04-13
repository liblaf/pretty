from __future__ import annotations

from typing import TYPE_CHECKING

import attrs

from liblaf.pretty._trace import TracedRef

from ._node_base import WrappedNode

if TYPE_CHECKING:
    from ._context import TraceContext


@attrs.define
class WrappedObject(WrappedNode):
    referencable: bool = attrs.field(default=True, kw_only=True)

    def visit(self, ctx: TraceContext) -> TracedRef | None:
        if (
            self.referencable
            and (anchor := ctx.trace_cache.get(self.identifier.id_)) is not None
        ):
            anchor.has_ref = True
            return TracedRef(identifier=self.identifier)
        return None
