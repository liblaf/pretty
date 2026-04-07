from __future__ import annotations

import abc
from typing import TYPE_CHECKING

from liblaf.pretty._trace import Traced

if TYPE_CHECKING:
    from ._context import TraceContext


class Spec(abc.ABC):
    @abc.abstractmethod
    def trace(self, ctx: TraceContext, depth: int) -> Traced: ...
