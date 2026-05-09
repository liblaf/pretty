import functools
from collections.abc import Iterable
from typing import Self

import attrs
from rich.console import Console, ConsoleOptions, RenderableType
from rich.containers import Renderables
from rich.segment import Segment
from rich.text import Text

from liblaf.pretty.compile import Compiled, Constraints, Segments


def _default_console() -> Console:
    return Console(soft_wrap=True, markup=False, emoji=False, highlight=False)


@attrs.frozen
class CompileContext:
    console: Console = attrs.field(factory=_default_console)
    column: int = attrs.field(default=0, kw_only=True)
    constraints: Constraints = attrs.field(factory=Constraints, kw_only=True)
    prefix: Segments = attrs.field(factory=Segments, kw_only=True)

    def _default_options(self) -> ConsoleOptions:
        return self.console.options.update(
            overflow="ignore", no_wrap=True, highlight=False, markup=False
        )

    _options: ConsoleOptions = attrs.field(
        default=attrs.Factory(_default_options, takes_self=True), alias="options"
    )

    @property
    def options(self) -> ConsoleOptions:
        return self._options.update(
            max_width=self._options.max_width - self.prefix.width
        )

    @property
    def remaining_width(self) -> int:
        return self._options.max_width - max(self.column, self.prefix.width)

    def compile(
        self,
        *renderables: RenderableType,
        break_before: bool = False,
        break_after: bool = False,
    ) -> Compiled:
        return Compiled.from_segments(
            self.render(*renderables),
            break_before=break_before,
            break_after=break_after,
        )

    def fits(self, compiled: Compiled) -> bool:
        return (
            max(self.column, self.prefix.width) + compiled.lines[0].width
            <= self._options.max_width
        ) and (self.prefix.width + compiled.width <= self._options.max_width)

    def write(self, compiled: Compiled) -> Self:
        return attrs.evolve(self, column=self.column + compiled.width)

    def render(self, *renderables: RenderableType) -> Iterable[Segment]:
        renderables: list[RenderableType] = [
            _patch_renderable(renderable) for renderable in renderables
        ]
        return self.console.render(Renderables(renderables), options=self.options)


@functools.singledispatch
def _patch_renderable(renderable: RenderableType) -> RenderableType:
    return renderable


@_patch_renderable.register(str)
def _patch_renderable_str(renderable: str) -> Text:
    return Text(renderable, overflow="ignore", no_wrap=True, end="")


@_patch_renderable.register(Text)
def _patch_renderable_text(renderable: Text) -> Text:
    renderable: Text = renderable.copy()
    renderable.overflow = "ignore"
    renderable.no_wrap = True
    renderable.end = ""
    return renderable
