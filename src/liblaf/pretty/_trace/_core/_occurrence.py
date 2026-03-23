from __future__ import annotations

from typing import TYPE_CHECKING

import attrs

from liblaf.pretty._compile import Lowered

from ._items import LowerableChild
from ._nodes import TracedNode

if TYPE_CHECKING:
    from liblaf.pretty._lower._lowerer import Lowerer


@attrs.define
class TracedOccurrence(LowerableChild):
    node: TracedNode
    kind: str
    path: tuple[int, ...]
    depth: int
    ancestors: tuple[int, ...] = attrs.field(factory=tuple, repr=False)

    def lower(
        self,
        lowerer: Lowerer,
        *,
        inline_repeat: bool = False,
        ancestors: tuple[int, ...] = (),
    ) -> Lowered:
        node = self.node
        if inline_repeat:
            if node.obj_id in ancestors or node.referable:
                return lowerer.lower_reference(node)
            return node.lower(lowerer, inline_repeat=True, ancestors=ancestors)
        if self.kind == "cycle" or (self.kind == "repeat" and node.referable):
            return lowerer.lower_reference(node)
        annotate = (
            self.kind == "anchor" and node.referable and node.appearance_count > 1
        )
        return node.lower(
            lowerer,
            inline_repeat=self.kind == "repeat",
            ancestors=ancestors,
            annotate=annotate,
        )


@attrs.define
class TraceResult:
    root: TracedOccurrence
    nodes_by_id: dict[int, TracedNode]
    tracked_types: set[type]
