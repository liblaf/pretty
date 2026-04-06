import abc

import attrs
from rich.text import Text

from liblaf.pretty._const import EMPTY
from liblaf.pretty._trace import TracedItem

from ._context import TraceContext


@attrs.define
class SpecItem(abc.ABC):
    prefix: Text = attrs.field(default=EMPTY, kw_only=True)
    suffix: Text = attrs.field(default=EMPTY, kw_only=True)

    @abc.abstractmethod
    def trace(self, ctx: TraceContext) -> TracedItem: ...
