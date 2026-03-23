import contextlib
import functools
from collections.abc import Generator
from typing import cast

import attrs
import rich.segment
from rich.console import Console, ConsoleOptions, RenderableType, RenderResult
from rich.segment import Segment
from rich.text import Text

type Renderable = RenderableType | Segment | None


class Segments(rich.segment.Segments):
    @functools.cached_property
    def width(self) -> int:
        return sum(segment.cell_length for segment in self.segments)


@attrs.define
class Writer:
    console: Console = attrs.field(factory=rich.get_console)

    def _default_options(self) -> ConsoleOptions:
        return self.console.options.update(
            overflow="ignore", no_wrap=True, highlight=False, markup=False
        )

    _options: ConsoleOptions = attrs.field(
        default=attrs.Factory(_default_options, takes_self=True)
    )

    column: int = attrs.field(default=0, init=False)
    prefix: Segments = attrs.field(factory=lambda: Segments([]), init=False)

    @property
    def options(self) -> ConsoleOptions:
        return self._options.update(
            max_width=self._options.max_width - self.prefix.width
        )

    @property
    def remaining_width(self) -> int:
        if self.column == 0:
            return self._options.max_width - self.prefix.width
        return self._options.max_width - self.column

    def ensure_newline(self) -> RenderResult:
        if self.column > 0:
            yield Segment.line()
            self.column = 0

    @contextlib.contextmanager
    def indent(self, indent: Renderable) -> Generator[None]:
        prev_prefix: Segments = self.prefix
        self.prefix: Segments = self._render(self.prefix, indent)
        try:
            yield
        finally:
            self.prefix: Segments = prev_prefix

    def write(self, *renderables: Renderable) -> RenderResult:
        segments: Segments = self._render(*renderables)
        for line_iterable, newline in Segment.split_lines_terminator(segments.segments):
            if self.column == 0:
                yield self.prefix
                if not newline:
                    self.column += self.prefix.width
            line: Segments = Segments(line_iterable)
            yield line
            if newline:
                yield Segment.line()
                self.column = 0
            else:
                self.column += line.width

    def _render(self, *renderables: Renderable) -> Segments:
        segments: list[Segment] = []
        for renderable in renderables:
            segments.extend(self._render_one(renderable))
        return Segments(segments)

    @functools.singledispatchmethod
    def _render_one(self, renderable: object) -> list[Segment]:
        rich_renderable = cast("RenderableType", renderable)
        return list(self.console.render(rich_renderable, options=self._options))

    @_render_one.register(type(None))
    def _render_none(self, _renderable: None) -> list[Segment]:
        return []

    @_render_one.register(Segment)
    def _render_segment(self, renderable: Segment) -> list[Segment]:
        return [renderable]

    @_render_one.register(Text)
    def _render_text(self, renderable: Text) -> list[Segment]:
        renderable = renderable.copy()
        renderable.overflow = "ignore"
        renderable.no_wrap = True
        renderable.end = ""
        return list(self.console.render(renderable, options=self._options))

    @_render_one.register(str)
    def _render_str(self, renderable: str) -> list[Segment]:
        return [Segment(renderable)]
