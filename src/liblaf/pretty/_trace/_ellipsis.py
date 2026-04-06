from typing import override

import attrs

from liblaf.pretty._const import ELLIPSIS
from liblaf.pretty._lower import Lowered, LoweredLeaf

from ._context import LowerContext
from ._traced import Traced


@attrs.frozen
class TracedEllipsis(Traced):
    cls: type = attrs.field(default=None, init=False)
    id_: int = attrs.field(default=0, init=False)

    @override
    def lower(self, ctx: LowerContext) -> Lowered:
        return LoweredLeaf(value=ELLIPSIS)


TRACED_ELLIPSIS = TracedEllipsis()
