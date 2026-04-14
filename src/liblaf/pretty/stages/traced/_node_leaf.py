from typing import Self, override

import attrs
from rich.text import Text

from liblaf.pretty.common import ObjectIdentifier
from liblaf.pretty.literals import ELLIPSIS
from liblaf.pretty.stages.lowered import LoweredLeaf

from ._context import LowerContext
from ._node_object import TracedObject


@attrs.define
class TracedLeaf(TracedObject):
    value: Text

    @classmethod
    def ellipsis(cls) -> Self:
        return cls(ELLIPSIS, has_ref=False, identifier=ObjectIdentifier.from_obj(...))

    @classmethod
    def literal(cls, text: Text) -> Self:
        return cls(text, has_ref=False, identifier=ObjectIdentifier.missing())

    @override
    def lower(self, ctx: LowerContext) -> LoweredLeaf:
        annotation: Text = self.make_annotation(ctx)
        return LoweredLeaf(self.value, annotation=annotation)
