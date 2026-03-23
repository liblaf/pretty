import abc
import functools

import attrs
from rich.console import RenderResult
from rich.text import Text

from liblaf.pretty._compile._const import EMPTY
from liblaf.pretty._compile._writer import Writer


@attrs.define
class Item(abc.ABC):
    prefix: Text = attrs.field(default=EMPTY, kw_only=True)
    suffix: Text = attrs.field(default=EMPTY, kw_only=True)

    @functools.cached_property
    @abc.abstractmethod
    def width_inline(self) -> int | float:
        raise NotImplementedError

    @abc.abstractmethod
    def render(self, writer: Writer) -> RenderResult:
        raise NotImplementedError
