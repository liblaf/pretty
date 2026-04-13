from __future__ import annotations

import abc
from collections.abc import Callable, Iterable
from typing import TYPE_CHECKING, NamedTuple

import attrs

from liblaf.pretty._trace import Traced

if TYPE_CHECKING:
    from ._context import TraceContext


class Child(NamedTuple):
    wrapped: Wrapped
    depth: int
    attach: Callable[[Traced], None] | None


@attrs.define
class Wrapped(abc.ABC):
    @abc.abstractmethod
    def trace(self, ctx: TraceContext) -> tuple[Iterable[Child], Traced]: ...
