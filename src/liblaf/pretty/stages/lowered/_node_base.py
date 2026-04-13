import abc
import functools
from typing import override

import attrs
from rich.console import RenderResult
from rich.text import Text

from liblaf.pretty.literals import EMPTY

from ._base import Lowered
from ._renderer import Renderer


@attrs.frozen
class LoweredNode(Lowered):
    annotation: Text = attrs.field(default=EMPTY, kw_only=True)

    @override
    def render(self, renderer: Renderer) -> RenderResult:
        if self.width_flat + self.annotation.cell_len <= renderer.remaining_width:
            yield from self.render_flat(renderer, annotation=True)
        else:
            yield from self.render_break(renderer, annotation=True)
        yield from renderer.ensure_newline()

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
    def render_flat(
        self, renderer: Renderer, *, annotation: bool = False
    ) -> RenderResult:
        raise NotImplementedError

    @abc.abstractmethod
    def render_break(
        self, renderer: Renderer, *, annotation: bool = True
    ) -> RenderResult:
        raise NotImplementedError
