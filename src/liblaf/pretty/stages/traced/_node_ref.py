from typing import override

import attrs
from rich.text import Text

from liblaf.pretty.common import ObjectIdentifier
from liblaf.pretty.stages.lowered import LoweredLeaf

from ._context import LowerContext
from ._node_base import TracedNode


@attrs.define
class TracedRef(TracedNode):
    identifier: ObjectIdentifier

    @override
    def lower(self, ctx: LowerContext) -> LoweredLeaf:
        typename: str = ctx.get_ref_typename(self.identifier.cls)
        return LoweredLeaf(
            Text.assemble(
                ("<", "repr.tag_start"),
                (typename, "repr.tag_name"),
                (f" @ {self.identifier.id_:x}", "repr.tag_contents"),
                (">", "repr.tag_end"),
            )
        )
