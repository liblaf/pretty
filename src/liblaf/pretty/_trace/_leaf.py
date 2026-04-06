from typing import Self, override

import attrs
from rich.text import Text

from liblaf.pretty._const import ELLIPSIS
from liblaf.pretty._lower import LoweredLeaf

from ._context import LowerContext
from ._id import TraceId
from ._object import TracedObject


@attrs.define
class TracedLeaf(TracedObject):
    value: Text

    @classmethod
    def ellipsis(cls) -> Self:
        return cls(ELLIPSIS, annotated=False, ref=TraceId.from_obj(...))

    @override
    def lower(self, ctx: LowerContext) -> LoweredLeaf:
        annotation: Text = self.make_annotation(ctx)
        return LoweredLeaf(self.value, annotation=annotation)
