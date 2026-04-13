from typing import NoReturn, override

import attrs

from ._context import LowerContext
from ._node_base import TracedNode


@attrs.define
class TracedMissingType(TracedNode):
    @override
    def lower(self, ctx: LowerContext) -> NoReturn:
        raise NotImplementedError


TRACED_MISSING: TracedMissingType = TracedMissingType()
