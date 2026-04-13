import functools
from typing import override

import attrs
from rich.console import RenderResult
from rich.text import Text

from ._item_base import LoweredItem
from ._node_base import LoweredNode
from ._renderer import Renderer


@attrs.frozen
class LoweredContainer(LoweredNode):
    begin: Text
    children: list[LoweredItem]
    end: Text
    indent: Text

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
            + sum(item.width_inline for item in self.children)
            + self.end.cell_len
        )

    @override
    def render_flat(
        self, renderer: Renderer, *, annotation: bool = False
    ) -> RenderResult:
        yield from renderer.render(self.begin)
        for item in self.children:
            yield from item.render(renderer)
        yield from renderer.render(self.end)
        if annotation and self.annotation:
            yield from renderer.render(self.annotation)

    @override
    def render_break(
        self, renderer: Renderer, *, annotation: bool = True
    ) -> RenderResult:
        yield from renderer.render(self.begin)
        if annotation and self.annotation:
            yield from renderer.render(self.annotation)
        yield from renderer.ensure_newline()
        with renderer.indent(self.indent):
            for item in self.children:
                yield from item.render(renderer)
        yield from renderer.ensure_newline()
        yield from renderer.render(self.end)
