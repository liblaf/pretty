from __future__ import annotations

import abc
import functools
import math
from typing import TYPE_CHECKING, Self, override

import attrs
from rich.console import RenderResult
from rich.text import Text

from liblaf.pretty._const import EMPTY

from ._base import Lowered
from ._writer import Writer

if TYPE_CHECKING:
    from ._node import LoweredNode


@attrs.frozen
class LoweredItem(Lowered):
    prefix: Text = attrs.field(default=EMPTY, kw_only=True)
    suffix: Text = attrs.field(default=EMPTY, kw_only=True)

    @property
    @abc.abstractmethod
    def width_inline(self) -> int | float: ...


@attrs.frozen
class LoweredEntryItem(LoweredItem):
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
    def render(self, writer: Writer) -> RenderResult:
        if self._fits_inline(writer):
            yield from self._render_inline(writer)
        else:
            yield from writer.ensure_newline()
            if self._fits_flat_flat(writer):
                yield from self._render_flat_flat(writer)
            elif self._fits_flat_break(writer):
                yield from self._render_flat_break(writer)
            elif self._fits_break_flat(writer):
                yield from self._render_break_flat(writer)
            else:
                yield from self._render_break_break(writer)

    def _fits_inline(self, writer: Writer) -> bool:
        return (
            writer.column > 0
            and not self.key.annotation
            and not self.value.annotation
            and self.prefix.cell_len
            + self.key.width_flat
            + self.sep.cell_len
            + self.value.width_flat
            + self.suffix.cell_len
            <= writer.remaining_width
        )

    def _render_inline(self, writer: Writer) -> RenderResult:
        yield from writer.write(self.prefix)
        yield from self.key.render_flat(writer)
        yield from writer.write(self.sep)
        yield from self.value.render_flat(writer)
        yield from writer.write(self.suffix)

    def _fits_flat_flat(self, writer: Writer) -> bool:
        return (
            not self.key.annotation
            and self.key.width_flat
            + self.sep.cell_len
            + self.value.width_flat
            + self.suffix.cell_len
            + self.value.annotation.cell_len
            <= writer.remaining_width
        )

    def _render_flat_flat(self, writer: Writer) -> RenderResult:
        yield from self.key.render_flat(writer, annotation=False)
        yield from writer.write(self.sep)
        yield from self.value.render_flat(writer, annotation=False)
        yield from writer.write(self.suffix)
        if self.value.annotation:
            yield from writer.write(self.value.annotation)
            yield from writer.ensure_newline()

    def _fits_flat_break(self, writer: Writer) -> bool:
        return (
            not self.key.annotation
            and self.key.width_flat
            + self.sep.cell_len
            + self.value.width_break_begin
            + self.value.annotation.cell_len
            <= writer.remaining_width
        )

    def _render_flat_break(self, writer: Writer) -> RenderResult:
        yield from self.key.render_flat(writer, annotation=False)
        yield from writer.write(self.sep)
        yield from self.value.render_break(writer, annotation=True)
        yield from writer.write(self.suffix)
        yield from writer.ensure_newline()

    def _fits_break_flat(self, writer: Writer) -> bool:
        return (
            self.key.width_break_end
            + self.sep.cell_len
            + self.value.width_flat
            + self.suffix.cell_len
            + self.key.annotation.cell_len
            + self.value.annotation.cell_len
            <= writer.remaining_width
        )

    def _render_break_flat(self, writer: Writer) -> RenderResult:
        yield from self.key.render_break(writer, annotation=True)
        yield from writer.write(self.sep)
        yield from self.value.render_flat(writer, annotation=False)
        yield from writer.write(self.suffix)
        if self.value.annotation:
            yield from writer.write(self.value.annotation)
        yield from writer.ensure_newline()

    def _render_break_break(self, writer: Writer) -> RenderResult:
        yield from self.key.render_break(writer, annotation=True)
        yield from writer.write(self.sep)
        yield from self.value.render_break(writer, annotation=True)
        yield from writer.write(self.suffix)
        if self.key.annotation:
            yield from writer.write(self.key.annotation)
        yield from writer.ensure_newline()


@attrs.frozen
class LoweredValueItem(LoweredItem):
    value: LoweredNode

    @classmethod
    def ellipsis(cls, prefix: Text = EMPTY, suffix: Text = EMPTY) -> Self:
        from ._node import LoweredLeaf

        return cls(LoweredLeaf.ellipsis(), prefix=prefix, suffix=suffix)

    @functools.cached_property
    def width_inline(self) -> int | float:
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
            and self.width_inline <= writer.remaining_width
        )

    def _render_inline(self, writer: Writer) -> RenderResult:
        yield from writer.write(self.prefix)
        yield from self.value.render_flat(writer, annotation=False)
        yield from writer.write(self.suffix)

    def _fits_flat(self, writer: Writer) -> bool:
        return (
            self.value.width_flat
            + self.suffix.cell_len
            + self.value.annotation.cell_len
            <= writer.remaining_width
        )

    def _render_flat(self, writer: Writer) -> RenderResult:
        yield from self.value.render_flat(writer, annotation=False)
        yield from writer.write(self.suffix)
        if self.value.annotation:
            yield from writer.write(self.value.annotation)
            yield from writer.ensure_newline()

    def _render_break(self, writer: Writer) -> RenderResult:
        yield from self.value.render_break(writer, annotation=True)
        yield from writer.write(self.suffix)
        yield from writer.ensure_newline()
