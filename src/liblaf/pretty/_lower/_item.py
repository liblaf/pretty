import abc

import attrs
from rich.console import RenderResult
from rich.text import Text

from liblaf.pretty._const import EMPTY

from ._writer import Writer


@attrs.frozen
class LoweredItem(abc.ABC):
    prefix: Text = attrs.field(default=EMPTY, kw_only=True)
    suffix: Text = attrs.field(default=EMPTY, kw_only=True)

    @property
    @abc.abstractmethod
    def width_inline(self) -> int | float: ...

    @abc.abstractmethod
    def render(self, writer: Writer) -> RenderResult: ...
