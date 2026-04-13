import functools
import math
from typing import override

import attrs
from rich.console import RenderResult
from rich.text import Text

from ._item_base import LoweredItem
from ._node_base import LoweredNode
from ._renderer import Renderer


@attrs.frozen
class LoweredKeyValueItem(LoweredItem):
    key: LoweredNode
    sep: Text
    value: LoweredNode

    @functools.cached_property
    def width_inline(self) -> int | float:
        if self.key.annotation or self.value.annotation:
            return math.inf
        return (
            self.prefix.cell_len
            + self.key.width_flat
            + self.sep.cell_len
            + self.value.width_flat
            + self.suffix.cell_len
        )

    @override
    def render(self, renderer: Renderer) -> RenderResult:
        if self._fits_inline(renderer):
            yield from self._render_inline(renderer)
        else:
            yield from renderer.ensure_newline()
            if self._fits_flat_flat(renderer):
                yield from self._render_flat_flat(renderer)
            elif self._fits_flat_break(renderer):
                yield from self._render_flat_break(renderer)
            elif self._fits_break_flat(renderer):
                yield from self._render_break_flat(renderer)
            else:
                yield from self._render_break_break(renderer)

    def _fits_inline(self, renderer: Renderer) -> bool:
        return (
            renderer.column > 0
            and not self.key.annotation
            and not self.value.annotation
            and self.prefix.cell_len
            + self.key.width_flat
            + self.sep.cell_len
            + self.value.width_flat
            + self.suffix.cell_len
            <= renderer.remaining_width
        )

    def _render_inline(self, renderer: Renderer) -> RenderResult:
        yield from renderer.render(self.prefix)
        yield from self.key.render_flat(renderer)
        yield from renderer.render(self.sep)
        yield from self.value.render_flat(renderer)
        yield from renderer.render(self.suffix)

    def _fits_flat_flat(self, renderer: Renderer) -> bool:
        return (
            not self.key.annotation
            and self.key.width_flat
            + self.sep.cell_len
            + self.value.width_flat
            + self.suffix.cell_len
            + self.value.annotation.cell_len
            <= renderer.remaining_width
        )

    def _render_flat_flat(self, renderer: Renderer) -> RenderResult:
        yield from self.key.render_flat(renderer, annotation=False)
        yield from renderer.render(self.sep)
        yield from self.value.render_flat(renderer, annotation=False)
        yield from renderer.render(self.suffix)
        if self.value.annotation:
            yield from renderer.render(self.value.annotation)
            yield from renderer.ensure_newline()

    def _fits_flat_break(self, renderer: Renderer) -> bool:
        return (
            not self.key.annotation
            and self.key.width_flat
            + self.sep.cell_len
            + self.value.width_break_begin
            + self.value.annotation.cell_len
            <= renderer.remaining_width
        )

    def _render_flat_break(self, renderer: Renderer) -> RenderResult:
        yield from self.key.render_flat(renderer, annotation=False)
        yield from renderer.render(self.sep)
        yield from self.value.render_break(renderer, annotation=True)
        yield from renderer.render(self.suffix)
        yield from renderer.ensure_newline()

    def _fits_break_flat(self, renderer: Renderer) -> bool:
        return (
            self.key.width_break_end
            + self.sep.cell_len
            + self.value.width_flat
            + self.suffix.cell_len
            + self.key.annotation.cell_len
            + self.value.annotation.cell_len
            <= renderer.remaining_width
        )

    def _render_break_flat(self, renderer: Renderer) -> RenderResult:
        yield from self.key.render_break(renderer, annotation=True)
        yield from renderer.render(self.sep)
        yield from self.value.render_flat(renderer, annotation=False)
        yield from renderer.render(self.suffix)
        if self.value.annotation:
            yield from renderer.render(self.value.annotation)
        yield from renderer.ensure_newline()

    def _render_break_break(self, renderer: Renderer) -> RenderResult:
        yield from self.key.render_break(renderer, annotation=True)
        yield from renderer.render(self.sep)
        yield from self.value.render_break(renderer, annotation=True)
        yield from renderer.render(self.suffix)
        if self.key.annotation:
            yield from renderer.render(self.key.annotation)
        yield from renderer.ensure_newline()
