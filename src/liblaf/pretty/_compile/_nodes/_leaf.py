import functools
import math
from typing import override

import attrs
from rich.console import RenderResult
from rich.containers import Lines
from rich.text import Text

from liblaf.pretty._compile._writer import Writer

from ._base import Lowered


@attrs.define
class LoweredLeaf(Lowered):
    value: Text

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
    def render_flat(self, writer: Writer, *, annotation: bool = False) -> RenderResult:
        yield from self.render_break(writer, annotation=annotation)

    @override
    def render_break(self, writer: Writer, *, annotation: bool = True) -> RenderResult:
        if annotation and self.annotation:
            yield from writer.write(self.lines[0].rstrip())
            yield from writer.write(self.annotation)
            yield from writer.ensure_newline()
            yield from writer.write(Lines(self.lines[1:]))
        else:
            yield from writer.write(self.value)
