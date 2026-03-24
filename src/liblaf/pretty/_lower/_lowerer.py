from __future__ import annotations

import attrs

from liblaf.pretty._compile import LoweredLeaf
from liblaf.pretty._trace._model._nodes import TracedNode
from liblaf.pretty._trace._model._occurrence import TraceResult
from liblaf.pretty._types._doc import PrettyDoc
from liblaf.pretty._types._options import PrettyOptions

from ._context import LowerContext
from ._names import TypeNameResolver


@attrs.define
class Lowerer:
    result: TraceResult
    ctx: LowerContext

    def lower_root(self) -> PrettyDoc:
        return PrettyDoc(self.result.root.lower(self))

    def lower_reference(self, node: TracedNode) -> LoweredLeaf:
        return LoweredLeaf(
            self.ctx.reference_formatter.inline_ref(
                node.cls, node.obj_id, self.ctx.typenames
            )
        )


def lower(result: TraceResult, *, options: PrettyOptions) -> PrettyDoc:
    ctx = LowerContext(
        typenames=TypeNameResolver().resolve(result.tracked_types),
        indent=options.indent.copy(),
    )
    return Lowerer(result=result, ctx=ctx).lower_root()
