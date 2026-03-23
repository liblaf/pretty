from __future__ import annotations

import attrs

from .._api._config import PrettyOptions
from .._api._doc import PrettyDoc
from .._compile import Lowered, LoweredLeaf
from .._trace import TraceResult, TracedContainerNode, TracedLeafNode, TracedNode
from .._trace import TracedOccurrence
from ._container import lower_container
from ._context import LowerContext
from ._names import TypeNameResolver


@attrs.define
class Lowerer:
    result: TraceResult
    ctx: LowerContext

    def lower_root(self) -> PrettyDoc:
        return PrettyDoc(self.lower_occurrence(self.result.root))

    def lower_occurrence(
        self,
        occurrence: TracedOccurrence,
        *,
        inline_repeat: bool = False,
        ancestors: tuple[int, ...] = (),
    ) -> Lowered:
        node: TracedNode = occurrence.node
        if inline_repeat:
            if node.obj_id in ancestors or node.referable:
                return self._lower_reference(node)
            return self.lower_node(node, inline_repeat=True, ancestors=ancestors)
        if occurrence.kind == "cycle":
            return self._lower_reference(node)
        if occurrence.kind == "repeat" and node.referable:
            return self._lower_reference(node)
        annotate: bool = occurrence.kind == "anchor" and node.referable
        annotate = annotate and node.appearance_count > 1
        return self.lower_node(
            node,
            inline_repeat=occurrence.kind == "repeat",
            ancestors=ancestors,
            annotate=annotate,
        )

    def lower_node(
        self,
        node: TracedNode,
        *,
        inline_repeat: bool,
        ancestors: tuple[int, ...],
        annotate: bool = False,
    ) -> Lowered:
        match node:
            case TracedLeafNode(value=value):
                lowered: Lowered = LoweredLeaf(value.copy())
            case TracedContainerNode() as container:
                lowered = lower_container(
                    self,
                    container,
                    inline_repeat=inline_repeat,
                    ancestors=ancestors,
                )
            case _:
                raise TypeError(node)
        if annotate:
            lowered.annotation = self.ctx.reference_formatter.anchor_annotation(
                node.cls, node.obj_id, self.ctx.typenames
            )
        return lowered

    def _lower_reference(self, node: TracedNode) -> LoweredLeaf:
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
