from typing import override

import attrs
from rich.text import Text

from liblaf.pretty._lower import LoweredLeaf

from ._context import LowerContext
from ._id import TraceId
from ._traced import Traced


@attrs.define
class TracedRef(Traced):
    ref: TraceId

    @override
    def lower(self, ctx: LowerContext) -> LoweredLeaf:
        typename: str = ctx.get_ref_typename(self.ref.cls)
        return LoweredLeaf(
            Text.assemble(
                ("<", "repr.tag_start"),
                (typename, "repr.tag_name"),
                (f" @ {self.ref.id_:x}", "repr.tag_contents"),
                (">", "repr.tag_end"),
            )
        )
