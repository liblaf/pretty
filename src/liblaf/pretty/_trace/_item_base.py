import abc
from typing import override

import attrs
from rich.text import Text

from liblaf.pretty._lower import LoweredItem
from liblaf.pretty.literals import EMPTY

from ._base import Traced
from ._context import LowerContext


@attrs.define
class TracedItem(Traced):
    prefix: Text = attrs.field(default=EMPTY, kw_only=True)
    suffix: Text = attrs.field(default=EMPTY, kw_only=True)

    @override
    @abc.abstractmethod
    def lower(self, ctx: LowerContext) -> LoweredItem: ...
