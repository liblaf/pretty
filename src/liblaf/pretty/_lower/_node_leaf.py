import functools
import math
from typing import Self, override

import attrs
from rich.console import RenderResult
from rich.containers import Lines
from rich.text import Text

from liblaf.pretty.literals import ELLIPSIS

from ._node_base import LoweredNode
from ._renderer import Renderer


@attrs.frozen
class LoweredLeaf(LoweredNode):
    value: Text

    @classmethod
    def ellipsis(cls) -> Self:
        return cls(ELLIPSIS)

    @functools.cached_property
    def lines(self) -> Lines:
        return self.value.split(include_separator=True, allow_blank=True)

    @functools.cached_property
    @override
    def width_break_begin(self) -> int | float:
        return math.inf if len(self.lines) == 1 else self.lines[0].cell_len

    @functools.cached_property
    @override
    def width_break_end(self) -> int | float:
        return math.inf if len(self.lines) == 1 else self.lines[-1].cell_len

    @functools.cached_property
    @override
    def width_flat(self) -> int | float:
        return self.value.cell_len if len(self.lines) == 1 else math.inf

    @override
    def render_flat(
        self, renderer: Renderer, *, annotation: bool = False
    ) -> RenderResult:
        assert len(self.lines) == 1
        yield from renderer.render(self.value)
        if annotation and self.annotation:
            yield from renderer.render(self.annotation)
            yield from renderer.ensure_newline()

    @override
    def render_break(
        self, renderer: Renderer, *, annotation: bool = True
    ) -> RenderResult:
        if len(self.lines) == 1:
            yield from self.render_flat(renderer, annotation=annotation)
        elif annotation and self.annotation:
            first_line: Text = self.lines[0].copy()
            first_line.rstrip()
            yield from renderer.render(first_line)
            yield from renderer.render(self.annotation)
            yield from renderer.ensure_newline()
            for line in self.lines[1:]:
                yield from renderer.render(line)
        else:
            yield from renderer.render(self.value)
