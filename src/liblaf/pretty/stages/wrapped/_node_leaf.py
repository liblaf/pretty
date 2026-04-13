from typing import Self, override

import attrs
from rich.text import Text

from liblaf.pretty.common import ObjectIdentifier
from liblaf.pretty.literals import ELLIPSIS
from liblaf.pretty.stages.traced import TracedLeaf, TracedNode

from ._context import TraceContext
from ._node_object import WrappedObject


@attrs.define
class WrappedLeaf(WrappedObject):
    value: Text

    @classmethod
    def ellipsis(cls) -> Self:
        return cls(
            value=ELLIPSIS, identifier=ObjectIdentifier.missing(), referencable=False
        )

    @override
    def trace(self, ctx: TraceContext) -> tuple[tuple[()], TracedNode]:
        if (ref := self.visit(ctx)) is not None:
            return (), ref
        traced = TracedLeaf(value=self.value, identifier=self.identifier)
        return (), traced
