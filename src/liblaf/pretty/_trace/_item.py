import abc
from typing import override

import attrs
from rich.text import Text

from liblaf.pretty._const import EMPTY
from liblaf.pretty._lower import LoweredItem

from ._context import LowerContext
from ._traced import Traced


@attrs.define
class TracedItem(Traced):
    prefix: Text = attrs.field(default=EMPTY, kw_only=True)
    suffix: Text = attrs.field(default=EMPTY, kw_only=True)

    @abc.abstractmethod
    @override
    def lower(self, ctx: LowerContext) -> LoweredItem: ...
