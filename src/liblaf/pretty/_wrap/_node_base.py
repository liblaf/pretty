from __future__ import annotations

import abc
from collections.abc import Iterable
from typing import TYPE_CHECKING, override

import attrs

from liblaf.pretty._trace import ObjectIdentifier, TracedNode

from ._base import Child, Wrapped

if TYPE_CHECKING:
    from ._context import TraceContext


@attrs.define
class WrappedNode(Wrapped):
    identifier: ObjectIdentifier = attrs.field(kw_only=True)

    @override
    @abc.abstractmethod
    def trace(self, ctx: TraceContext) -> tuple[Iterable[Child], TracedNode]: ...
