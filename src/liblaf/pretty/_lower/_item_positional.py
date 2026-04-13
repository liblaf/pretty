import functools
import math
from typing import Self, override

import attrs
from rich.console import RenderResult
from rich.text import Text

from liblaf.pretty.literals import EMPTY

from ._item_base import LoweredItem
from ._node_base import LoweredNode
from ._node_leaf import LoweredLeaf
from ._renderer import Renderer


@attrs.frozen
class LoweredPositionalItem(LoweredItem):
    value: LoweredNode

    @classmethod
    def ellipsis(cls, *, prefix: Text = EMPTY, suffix: Text = EMPTY) -> Self:
        return cls(LoweredLeaf.ellipsis(), prefix=prefix, suffix=suffix)

    @functools.cached_property
    def width_inline(self) -> int | float:
        if self.value.annotation:
            return math.inf
        return self.prefix.cell_len + self.value.width_flat + self.suffix.cell_len

    @override
    def render(self, renderer: Renderer) -> RenderResult:
        if self._fits_inline(renderer):
            yield from self._render_inline(renderer)
        else:
            yield from renderer.ensure_newline()
            if self._fits_flat(renderer):
                yield from self._render_flat(renderer)
            else:
                yield from self._render_break(renderer)

    def _fits_inline(self, renderer: Renderer) -> bool:
        return (
            renderer.column > 0
            and not self.value.annotation
            and self.width_inline <= renderer.remaining_width
        )

    def _render_inline(self, renderer: Renderer) -> RenderResult:
        yield from renderer.render(self.prefix)
        yield from self.value.render_flat(renderer, annotation=False)
        yield from renderer.render(self.suffix)

    def _fits_flat(self, renderer: Renderer) -> bool:
        return (
            self.value.width_flat
            + self.suffix.cell_len
            + self.value.annotation.cell_len
            <= renderer.remaining_width
        )

    def _render_flat(self, renderer: Renderer) -> RenderResult:
        yield from self.value.render_flat(renderer, annotation=False)
        yield from renderer.render(self.suffix)
        if self.value.annotation:
            yield from renderer.render(self.value.annotation)
            yield from renderer.ensure_newline()

    def _render_break(self, renderer: Renderer) -> RenderResult:
        yield from self.value.render_break(renderer, annotation=True)
        yield from renderer.render(self.suffix)
        yield from renderer.ensure_newline()
