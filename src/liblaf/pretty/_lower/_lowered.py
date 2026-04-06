import abc
import functools

import attrs
from rich.console import Console, ConsoleOptions, RenderResult
from rich.text import Text

from liblaf.pretty._const import EMPTY

from ._writer import Writer


@attrs.define
class Lowered(abc.ABC):
    annotation: Text = attrs.field(default=EMPTY, kw_only=True)

    def __rich_console__(
        self, console: Console, options: ConsoleOptions
    ) -> RenderResult:
        writer = Writer(console, options)
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
