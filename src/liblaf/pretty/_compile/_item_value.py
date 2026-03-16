import functools
import math
from typing import override

import attrs
from rich.console import RenderResult

from ._item import Item
from ._lowered import Lowered
from ._writer import Writer


@attrs.define
class ItemValue(Item):
    value: Lowered

    @functools.cached_property
    @override
    def width_flat(self) -> int | float:
        if self.value.annotation:
            return math.inf
        return self.prefix.cell_len + self.value.width_flat + self.suffix.cell_len

    @override
    def render(self, writer: Writer) -> RenderResult:
        if self._fits_inline(writer):
            yield from self._render_inline(writer)
        else:
            yield from writer.ensure_newline()
            if self._fits_flat(writer):
                yield from self._render_flat(writer)
            else:
                yield from self._render_break(writer)

    def _fits_inline(self, writer: Writer) -> bool:
        return (
            writer.column > 0
            and not self.value.annotation
            and self.prefix.cell_len + self.value.width_flat + self.suffix.cell_len
            <= writer.remaining_width
        )

    def _render_inline(self, writer: Writer) -> RenderResult:
        yield from writer.write(self.prefix)
        yield from self.value.render_flat(writer)
        yield from writer.write(self.suffix)

    def _fits_flat(self, writer: Writer) -> bool:
        return (
            self.prefix.cell_len
            + self.value.width_flat
            + self.suffix.cell_len
            + self.value.annotation.cell_len
            <= writer.remaining_width
        )

    def _render_flat(self, writer: Writer) -> RenderResult:
        yield from self.value.render_flat(writer)
        yield from writer.write(self.suffix)
        if self.value.annotation:
            yield from writer.write(self.value.annotation)
            yield from writer.ensure_newline()

    def _render_break(self, writer: Writer) -> RenderResult:
        yield from self.value.render_break(writer)
        yield from writer.write(self.suffix)
