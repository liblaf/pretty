from typing import Self

import attrs
from rich.text import Text

from liblaf.pretty.literals import EMPTY

from ._base import Lowered


@attrs.frozen
class LoweredItem:
    wrapped: Lowered
    flat_break: Text = attrs.field(default=EMPTY)

    def append(self, text: Text) -> Self:
        return attrs.evolve(self, wrapped=self.wrapped.append(text))
