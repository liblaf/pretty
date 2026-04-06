from typing import override

import attrs

from liblaf.pretty._lower import LoweredLeaf

from ._context import LowerContext
from ._traced import Traced


@attrs.frozen
class TracedRef(Traced):
    @override
    def lower(self, ctx: LowerContext) -> LoweredLeaf:
        return LoweredLeaf(ctx.make_ref(self.cls, self.id_))
