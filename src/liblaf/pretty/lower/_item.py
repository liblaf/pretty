import attrs
from rich.text import Text

from liblaf.pretty.literals import EMPTY

from ._base import Lowered


@attrs.frozen
class LoweredItem:
    wrapped: Lowered
    separator: Text = attrs.field(default=EMPTY)
