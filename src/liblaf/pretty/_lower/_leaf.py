from typing import override

import attrs
from rich.text import Text

from liblaf.pretty._compile import LoweredLeaf

from ._base import LowerContext, Traced
from ._reference import TracedReferent


@attrs.define
class TracedLeaf(Traced):
    value: Text

    @override
    def lower(self, ctx: LowerContext) -> LoweredLeaf:
        return LoweredLeaf(self.value)


@attrs.define
class TracedReferentLeaf(TracedReferent):
    value: Text

    @override
    def lower_referent(self, ctx: LowerContext) -> LoweredLeaf:
        return LoweredLeaf(self.value)
