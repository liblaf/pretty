import abc

import attrs
from rich.text import Text

from liblaf.pretty._const import EMPTY

from ._lowered import Lowered


@attrs.frozen
class LoweredItem(Lowered):
    prefix: Text = attrs.field(default=EMPTY, kw_only=True)
    suffix: Text = attrs.field(default=EMPTY, kw_only=True)

    @property
    @abc.abstractmethod
    def width_inline(self) -> int | float: ...
