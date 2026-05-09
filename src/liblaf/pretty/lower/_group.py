from collections.abc import Sequence
from typing import override

import attrs

from liblaf.pretty.compile import Compiled, Constraints, Flags

from ._base import Layout, Lowered
from ._context import CompileContext
from ._item import LoweredItem


@attrs.frozen
class Group(Lowered):
    children: Sequence[LoweredItem]


class GroupFlat(Layout):
    wrapped: Group

    @override
    def compile(self, ctx: CompileContext) -> Compiled:
        compiled: Compiled = Compiled()
        for child in self.wrapped.children:
            for layout in child.wrapped.filter_layouts(Constraints.INLINE):
                compiled += layout.compile(ctx) + ctx.render(child.separator)
                break
        return compiled

    @override
    def flags(self) -> Flags:
        return Flags(multiline=False)

    @override
    def satisfies(self, constraints: Constraints) -> bool:
        return super().satisfies(constraints) and all(
            child.wrapped.satisfies(Constraints.INLINE)
            for child in self.wrapped.children
        )
