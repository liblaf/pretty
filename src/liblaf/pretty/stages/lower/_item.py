import functools
from typing import Self, override

import attrs
from rich.text import Text

from liblaf.pretty.literals import EMPTY
from liblaf.pretty.stages.compile import CompileContext, Constraints, Flags

from ._base import Layout, Lowered


@attrs.frozen
class LoweredItem(Lowered):
    wrapped: Lowered
    flat_gap: Text = attrs.field(default=EMPTY)

    @functools.cached_property
    @override
    def layouts(self) -> list[Layout]:
        return [LoweredItemFlat(self), LoweredItemBreak(self)]

    @override
    def append(self, text: Text) -> Self:
        return attrs.evolve(self, wrapped=self.wrapped.append(text))


@attrs.frozen
class LoweredItemFlat(Layout):
    wrapped: LoweredItem

    @functools.cached_property
    @override
    def flags(self) -> Flags:
        return Flags.INLINE

    @override
    def print(self, ctx: CompileContext) -> None:
        self.wrapped.wrapped.print(ctx, Constraints.INLINE)
        ctx.print(self.wrapped.flat_gap)


@attrs.frozen
class LoweredItemBreak(Layout):
    wrapped: LoweredItem

    @functools.cached_property
    @override
    def flags(self) -> Flags:
        return Flags(multiline=True, break_after=True)

    @override
    def print(self, ctx: CompileContext) -> None:
        self.wrapped.wrapped.print(ctx, Constraints.BLOCK)
