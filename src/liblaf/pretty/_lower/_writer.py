from __future__ import annotations

import contextlib
import functools
from collections.abc import Generator

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
    console: Console = attrs.field(factory=Console)

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
        previous_prefix: Segments = self.prefix
        self.prefix = self._render(self.prefix, indent)
        try:
            yield
        finally:
            self.prefix = previous_prefix

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
            match renderable:
                case None:
                    pass
                case Segment():
                    segments.append(renderable)
                case Text():
                    renderable.overflow = "ignore"
                    renderable.no_wrap = True
                    renderable.end = ""
                    segments.extend(
                        self.console.render(renderable, options=self._options)
                    )
                case str(text):
                    segments.append(Segment(text))
                case renderable:
                    segments.extend(
                        self.console.render(renderable, options=self._options)
                    )
        return Segments(segments)
