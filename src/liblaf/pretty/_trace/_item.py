import abc

import attrs
from rich.text import Text

from liblaf.pretty._const import EMPTY
from liblaf.pretty._lower import LoweredItem

from ._context import LowerContext


@attrs.frozen
class TracedItem(abc.ABC):
    prefix: Text = attrs.field(default=EMPTY, kw_only=True)
    suffix: Text = attrs.field(default=EMPTY, kw_only=True)

    @abc.abstractmethod
    def lower(self, ctx: LowerContext) -> LoweredItem: ...
