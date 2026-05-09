import abc
from collections.abc import Iterable

from liblaf.pretty.compile import Compiled, Constraints, Flags

from ._context import CompileContext


class Layout(abc.ABC):
    @abc.abstractmethod
    def compile(self, ctx: CompileContext) -> Compiled: ...

    @abc.abstractmethod
    def flags(self) -> Flags: ...

    def satisfies(self, constraints: Constraints) -> bool:
        return constraints.allow(self.flags())


class Lowered(abc.ABC):
    def compile(self, ctx: CompileContext) -> Compiled | None:
        compiled: Compiled | None = None
        for layout in self.filter_layouts(ctx.constraints):
            compiled: Compiled = layout.compile(ctx)
            if ctx.fits(compiled):
                return compiled
        return compiled

    def filter_layouts(self, constraints: Constraints) -> Iterable[Layout]:
        for layout in self.layouts():
            if layout.satisfies(constraints):
                yield layout

    @abc.abstractmethod
    def layouts(self) -> Iterable[Layout]: ...

    def satisfies(self, constraints: Constraints) -> bool:
        for _ in self.filter_layouts(constraints):
            return True
        return False
