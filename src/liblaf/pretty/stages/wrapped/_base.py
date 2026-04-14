from __future__ import annotations

import abc
from collections.abc import Callable, Iterable
from typing import NamedTuple

import attrs

from liblaf.pretty.stages.traced import Traced

from ._context import TraceContext


class WrappedChild(NamedTuple):
    wrapped: Wrapped
    depth: int
    attach: Callable[[Traced], None]


@attrs.define
class Wrapped(abc.ABC):
    @abc.abstractmethod
    def trace(self, ctx: TraceContext) -> tuple[Iterable[WrappedChild], Traced]: ...
