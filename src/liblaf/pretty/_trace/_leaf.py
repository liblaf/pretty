from typing import override

import attrs
from rich.text import Text

from liblaf.pretty._lower import LoweredLeaf

from ._context import LowerContext
from ._object import TracedObject


@attrs.define
class TracedLeaf(TracedObject):
    value: Text

    @override
    def lower(self, ctx: LowerContext) -> LoweredLeaf:
        annotation: Text = self.make_annotation(ctx)
        return LoweredLeaf(self.value, annotation=annotation)
