from __future__ import annotations

import abc
import functools
import math
from typing import TYPE_CHECKING, override

import attrs
from rich.console import RenderResult
from rich.containers import Lines
from rich.text import Text

from liblaf.pretty._const import EMPTY

from ._base import Lowered
from ._writer import Writer

if TYPE_CHECKING:
    from ._item import LoweredItem


@attrs.frozen
class LoweredNode(Lowered):
    annotation: Text = attrs.field(default=EMPTY, kw_only=True)

    @override
    def render(self, writer: Writer) -> RenderResult:
        if self.width_flat <= writer.remaining_width:
            yield from self.render_flat(writer, annotation=True)
        else:
            yield from self.render_break(writer, annotation=True)

    @functools.cached_property
    @abc.abstractmethod
    def width_break_begin(self) -> int | float:
        raise NotImplementedError

    @functools.cached_property
    @abc.abstractmethod
    def width_break_end(self) -> int | float:
        raise NotImplementedError

    @functools.cached_property
    @abc.abstractmethod
    def width_flat(self) -> int | float:
        raise NotImplementedError

    @abc.abstractmethod
    def render_flat(self, writer: Writer, *, annotation: bool = False) -> RenderResult:
        raise NotImplementedError

    @abc.abstractmethod
    def render_break(self, writer: Writer, *, annotation: bool = True) -> RenderResult:
        raise NotImplementedError


@attrs.frozen
class LoweredContainer(LoweredNode):
    begin: Text
    items: list[LoweredItem]
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


@attrs.frozen
class LoweredLeaf(LoweredNode):
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
        assert len(self.lines) == 1
        yield from writer.write(self.value)
        if annotation and self.annotation:
            yield from writer.write(self.annotation)
            yield from writer.ensure_newline()

    @override
    def render_break(self, writer: Writer, *, annotation: bool = True) -> RenderResult:
        assert len(self.lines) > 1
        if annotation and self.annotation:
            first_line: Text = self.lines[0].copy()
            first_line.rstrip()
            yield from writer.write(first_line)
            yield from writer.write(self.annotation)
            yield from writer.ensure_newline()
            for line in self.lines[1:]:
                yield from writer.write(line)
        else:
            yield from writer.write(self.value)
