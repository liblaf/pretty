from __future__ import annotations

import abc
from typing import TYPE_CHECKING

import attrs

from liblaf.pretty._trace import Traced

if TYPE_CHECKING:
    from ._context import TraceContext


@attrs.define
class Spec[T: Traced](abc.ABC):
    @abc.abstractmethod
    def trace(self, ctx: TraceContext, depth: int) -> T: ...
