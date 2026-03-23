import functools
from collections.abc import Sequence
from typing import override

import attrs
from rich.console import RenderResult
from rich.text import Text

from .._const import INDENT
from .._items._base import Item
from .._writer import Writer
from ._base import Lowered


@attrs.define
class LoweredContainer(Lowered):
    begin: Text
    end: Text
    items: Sequence[Item]
    indent: Text = attrs.field(default=INDENT, kw_only=True)

    @functools.cached_property
    @override
    def width_break_begin(self) -> int | float:
        return self.begin.cell_len

    @functools.cached_property
    @override
    def width_break_end(self) -> int | float:
        return self.end.cell_len

    @functools.cached_property
    @override
    def width_flat(self) -> int | float:
        return (
            self.begin.cell_len
            + sum(item.width_inline for item in self.items)
            + self.end.cell_len
        )

    @override
    def render_flat(self, writer: Writer, *, annotation: bool = False) -> RenderResult:
        yield from writer.write(self.begin)
        for item in self.items:
            yield from item.render(writer)
        yield from writer.write(self.end)
        if annotation and self.annotation:
            yield from writer.write(self.annotation)

    @override
    def render_break(self, writer: Writer, *, annotation: bool = True) -> RenderResult:
        yield from writer.write(self.begin)
        if annotation and self.annotation:
            yield from writer.write(self.annotation)
        yield from writer.ensure_newline()
        with writer.indent(self.indent):
            for item in self.items:
                yield from item.render(writer)
        yield from writer.ensure_newline()
        yield from writer.write(self.end)
