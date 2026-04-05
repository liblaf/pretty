from __future__ import annotations

import abc
import functools
import math
from collections import Counter
from typing import Any

import attrs
from rich.console import Console, ConsoleOptions, RenderResult
from rich.containers import Lines
from rich.text import Text

from ._writer import Writer


@attrs.define
class LowerContext:
    indent: Text
    obj_id_counts: Counter[int]
    typenames: dict[type, str]

    def make_ref_text(self, cls: type, obj_id: int) -> Text:
        return Text.assemble(
            ("<", "repr.tag_start"),
            ("*", "repr.ellipsis"),
            (self.typenames[cls], "repr.tag_name"),
            (" object at ", "repr.tag_contents"),
            (hex(obj_id), "repr.number"),
            (">", "repr.tag_end"),
        )


@attrs.define
class Lowered(abc.ABC):
    annotation: Text = attrs.field(factory=Text, kw_only=True)

    def __rich_console__(
        self, console: Console, options: ConsoleOptions
    ) -> RenderResult:
        writer = Writer(console, options)
        if self.width_flat + self.annotation.cell_len <= options.max_width:
            yield from self.render_flat(writer, annotation=True)
        else:
            yield from self.render_break(writer, annotation=True)
        yield from writer.ensure_newline()

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
    def render_break(self, writer: Writer, *, annotation: bool = False) -> RenderResult:
        raise NotImplementedError


@attrs.define(kw_only=True)
class LoweredLeaf(Lowered):
    value: Text = attrs.field(converter=lambda value: value.copy())

    @functools.cached_property
    def lines(self) -> Lines:
        return self.value.split(include_separator=True, allow_blank=True)

    @functools.cached_property
    def width_break_begin(self) -> int | float:
        return math.inf if len(self.lines) == 1 else self.lines[0].cell_len

    @functools.cached_property
    def width_break_end(self) -> int | float:
        return math.inf if len(self.lines) == 1 else self.lines[-1].cell_len

    @functools.cached_property
    def width_flat(self) -> int | float:
        return self.value.cell_len if len(self.lines) == 1 else math.inf

    def render_flat(self, writer: Writer, *, annotation: bool = False) -> RenderResult:
        yield from self.render_break(writer, annotation=annotation)

    def render_break(self, writer: Writer, *, annotation: bool = True) -> RenderResult:
        if annotation and self.annotation:
            yield from writer.write(self.lines[0].rstrip())
            yield from writer.write(self.annotation)
            yield from writer.ensure_newline()
            yield from writer.write(Lines(self.lines[1:]))
        else:
            yield from writer.write(self.value)


@attrs.define(kw_only=True)
class LoweredContainer(Lowered):
    begin: Text = attrs.field(converter=lambda value: value.copy())
    end: Text = attrs.field(converter=lambda value: value.copy())
    items: list[Any] = attrs.field(factory=list)
    indent: Text = attrs.field(converter=lambda value: value.copy())

    @functools.cached_property
    def width_break_begin(self) -> int | float:
        return self.begin.cell_len

    @functools.cached_property
    def width_break_end(self) -> int | float:
        return self.end.cell_len

    @functools.cached_property
    def width_flat(self) -> int | float:
        return (
            self.begin.cell_len
            + sum(item.width_inline for item in self.items)
            + self.end.cell_len
        )

    def render_flat(self, writer: Writer, *, annotation: bool = False) -> RenderResult:
        yield from writer.write(self.begin)
        for item in self.items:
            yield from item.render(writer)
        yield from writer.write(self.end)
        if annotation and self.annotation:
            yield from writer.write(self.annotation)

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
